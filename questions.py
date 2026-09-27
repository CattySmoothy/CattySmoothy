from flask import render_template, request, jsonify, abort

from extensions import db
from models import Question
from commission_board import owner_required

MAX_NAME = 80
MAX_EMAIL = 255
MAX_MESSAGE = 2000


def register_question_routes(app):
    @app.route('/support/ask', methods=['POST'])
    def ask_question():
        data = request.get_json(silent=True) or {}
        name = (data.get('name') or '').strip()[:MAX_NAME]
        email = (data.get('email') or '').strip()[:MAX_EMAIL]
        message = (data.get('message') or '').strip()

        if not message or len(message) > MAX_MESSAGE:
            return jsonify({'error': 'Enter your question (max 2000 characters).'}), 400

        db.session.add(Question(name=name or None, email=email or None, message=message))
        db.session.commit()
        return jsonify({'ok': True}), 201

    @app.route('/questions')
    @owner_required
    def questions_inbox():
        items = Question.query.order_by(Question.answered, Question.created_at.desc()).all()
        return render_template('questions.html', title="Questions",
                                questions=[q.to_dict() for q in items])

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
