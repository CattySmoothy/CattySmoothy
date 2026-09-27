from datetime import datetime, date
from functools import wraps

from flask import render_template, request, jsonify, abort
from flask_login import current_user

from extensions import db
from models import Commission, CommissionTask, EarningsGoal, Question, OWNER_EMAIL

MAX_NAME = 100
MAX_TITLE = 150
MAX_TASK = 150
MAX_TEXT = 4000


def owner_required(view):
    """Restrict a route to the one account running the site. Everyone else —
    including a logged-out visitor — gets a plain 404 rather than a redirect
    to login, so the page's existence isn't revealed to anyone but its
    owner, the same way the donors admin key is hidden rather than merely
    refused."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or current_user.email != OWNER_EMAIL:
            abort(404)
        return view(*args, **kwargs)
    return wrapped


def _parse_price(raw):
    if raw in (None, ''):
        return None
    try:
        value = round(float(raw), 2)
    except (TypeError, ValueError):
        return None
    return value if 0 <= value < 1_000_000 else None


def _parse_date(raw):
    if not raw:
        return None
    try:
        return datetime.strptime(raw, '%Y-%m-%d').date()
    except ValueError:
        return None


def _commission_or_404(commission_id):
    commission = db.session.get(Commission, commission_id)
    if not commission:
        abort(404)
    return commission


def register_commission_board_routes(app):
    @app.route('/queue')
    @owner_required
    def commission_queue():
        commissions = Commission.query.order_by(Commission.position, Commission.created_at).all()
        goal = EarningsGoal.query.order_by(EarningsGoal.id.desc()).first()
        questions = Question.query.order_by(Question.answered, Question.created_at.desc()).all()
        return render_template(
            'queue.html',
            title="Commissions",
            statuses=Commission.STATUSES,
            commissions=[c.to_dict() for c in commissions],
            goal_amount=float(goal.amount) if goal else None,
            today=date.today().isoformat(),
            questions=[q.to_dict() for q in questions],
        )

    @app.route('/queue/goal', methods=['PATCH'])
    @owner_required
    def update_earnings_goal():
        data = request.get_json(silent=True) or {}
        amount = _parse_price(data.get('amount'))
        if amount is None:
            return jsonify({'error': 'Enter a goal amount.'}), 400
        db.session.add(EarningsGoal(amount=amount))
        db.session.commit()
        return jsonify({'amount': amount})

    @app.route('/queue/commissions', methods=['POST'])
    @owner_required
    def create_commission():
        data = request.get_json(silent=True) or {}
        client_name = (data.get('client_name') or '').strip()
        title = (data.get('title') or '').strip()
        if not client_name or len(client_name) > MAX_NAME:
            return jsonify({'error': 'Enter a client name (max 100 characters).'}), 400
        if not title or len(title) > MAX_TITLE:
            return jsonify({'error': 'Enter a piece title (max 150 characters).'}), 400

        status = data.get('status') if data.get('status') in Commission.STATUSES else 'queued'
        top = db.session.query(db.func.min(Commission.position)).filter_by(status=status).scalar()
        commission = Commission(
            client_name=client_name,
            title=title,
            description=(data.get('description') or '').strip()[:MAX_TEXT],
            price=_parse_price(data.get('price')),
            status=status,
            deadline=_parse_date(data.get('deadline')),
            notes=(data.get('notes') or '').strip()[:MAX_TEXT],
            position=(top - 1) if top is not None else 0,
        )
        db.session.add(commission)
        db.session.commit()
        return jsonify({'commission': commission.to_dict()}), 201

    @app.route('/queue/commissions/<int:commission_id>', methods=['PATCH'])
    @owner_required
    def update_commission(commission_id):
        commission = _commission_or_404(commission_id)
        data = request.get_json(silent=True) or {}

        if 'client_name' in data:
            name = (data['client_name'] or '').strip()
            if not name or len(name) > MAX_NAME:
                return jsonify({'error': 'Enter a client name (max 100 characters).'}), 400
            commission.client_name = name
        if 'title' in data:
            title = (data['title'] or '').strip()
            if not title or len(title) > MAX_TITLE:
                return jsonify({'error': 'Enter a piece title (max 150 characters).'}), 400
            commission.title = title
        if 'description' in data:
            commission.description = (data['description'] or '').strip()[:MAX_TEXT]
        if 'notes' in data:
            commission.notes = (data['notes'] or '').strip()[:MAX_TEXT]
        if 'price' in data:
            commission.price = _parse_price(data['price'])
        if 'deadline' in data:
            commission.deadline = _parse_date(data['deadline'])
        if 'status' in data:
            if data['status'] not in Commission.STATUSES:
                return jsonify({'error': 'Unknown status.'}), 400
            commission.status = data['status']
        if 'position' in data:
            try:
                commission.position = int(data['position'])
            except (TypeError, ValueError):
                return jsonify({'error': 'Invalid position.'}), 400

        db.session.commit()
        return jsonify({'commission': commission.to_dict()})

    @app.route('/queue/commissions/<int:commission_id>', methods=['DELETE'])
    @owner_required
    def delete_commission(commission_id):
        commission = _commission_or_404(commission_id)
        db.session.delete(commission)
        db.session.commit()
        return jsonify({'deleted': commission_id})

    @app.route('/queue/commissions/<int:commission_id>/tasks', methods=['POST'])
    @owner_required
    def add_commission_task(commission_id):
        commission = _commission_or_404(commission_id)
        data = request.get_json(silent=True) or {}
        label = (data.get('label') or '').strip()
        if not label or len(label) > MAX_TASK:
            return jsonify({'error': 'Enter a task (max 150 characters).'}), 400

        bottom = db.session.query(db.func.max(CommissionTask.position)) \
            .filter_by(commission_id=commission.id).scalar()
        task = CommissionTask(commission_id=commission.id, label=label,
                               position=(bottom + 1) if bottom is not None else 0)
        db.session.add(task)
        db.session.commit()
        return jsonify({'task': task.to_dict(), 'commission': commission.to_dict()}), 201

    @app.route('/queue/tasks/<int:task_id>', methods=['PATCH'])
    @owner_required
    def update_commission_task(task_id):
        task = db.session.get(CommissionTask, task_id)
        if not task:
            abort(404)
        data = request.get_json(silent=True) or {}
        if 'label' in data:
            label = (data['label'] or '').strip()
            if not label or len(label) > MAX_TASK:
                return jsonify({'error': 'Enter a task (max 150 characters).'}), 400
            task.label = label
        if 'done' in data:
            task.done = bool(data['done'])
        db.session.commit()
        return jsonify({'task': task.to_dict(), 'commission': task.commission.to_dict()})

    @app.route('/queue/tasks/<int:task_id>', methods=['DELETE'])
    @owner_required
    def delete_commission_task(task_id):
        task = db.session.get(CommissionTask, task_id)
        if not task:
            abort(404)
        commission = task.commission
        db.session.delete(task)
        db.session.commit()
        return jsonify({'deleted': task_id, 'commission': commission.to_dict()})
