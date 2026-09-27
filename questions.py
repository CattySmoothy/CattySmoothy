from flask import request, jsonify, abort, redirect, url_for
from flask_login import login_required, current_user

from extensions import db
from models import Question
from commission_board import owner_required

MAX_MESSAGE = 2000


def register_question_routes(app):
    @app.route('/support/ask', methods=['POST'])
    @login_required
    def ask_question():
        data = request.get_json(silent=True) or {}
        message = (data.get('message') or '').strip()

        if not message or len(message) > MAX_MESSAGE:
            return jsonify({'error': 'Enter your question (max 2000 characters).'}), 400

        q = Question(user_id=current_user.id, message=message)
        db.session.add(q)
        db.session.commit()
        return jsonify({'question': q.to_dict()}), 201

    @app.route('/questions')
    @owner_required
    def questions_inbox():
        # Questions now live on the Commissions (queue) page rather than
        # their own tab — keep the URL alive as a redirect.
        return redirect(url_for('commission_queue') + '#questions')

    @app.route('/questions/<int:question_id>', methods=['PATCH'])
    @owner_required
    def update_question(question_id):
        q = db.session.get(Question, question_id)
        if not q:
            abort(404)
        data = request.get_json(silent=True) or {}
        if 'answered' in data:
            q.answered = bool(data['answered'])
        db.session.commit()
        return jsonify({'question': q.to_dict()})

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @owner_required
    def delete_question(question_id):
        q = db.session.get(Question, question_id)
        if not q:
            abort(404)
        db.session.delete(q)
        db.session.commit()
        return jsonify({'deleted': question_id})
