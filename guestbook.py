from flask import request, jsonify
from flask_login import login_required, current_user

from extensions import db
from models import GuestbookEntry

MAX_DISPLAY_NAME_LENGTH = 50
MAX_MESSAGE_LENGTH = 300


def register_guestbook_routes(app):
    @app.route('/guestbook', methods=['POST'])
    @login_required
    def sign_guestbook():
        data = request.get_json(silent=True) or {}
        display_name = (data.get('display_name') or '').strip()
        message = (data.get('message') or '').strip()

        if not display_name or len(display_name) > MAX_DISPLAY_NAME_LENGTH:
            return jsonify({'error': 'Please enter a display name (max 50 characters).'}), 400
        if not message or len(message) > MAX_MESSAGE_LENGTH:
            return jsonify({'error': 'Please enter a message (max 300 characters).'}), 400

        entry = GuestbookEntry(user_id=current_user.id, display_name=display_name, message=message)
        db.session.add(entry)
        db.session.commit()

        return jsonify({'entry': {
            'display_name': entry.display_name,
            'message': entry.message,
            'created_at': entry.created_at.strftime('%b %d, %Y'),
        }}), 201
