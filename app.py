import os
from flask import Flask, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from flask_migrate import Migrate
import stripe

from extensions import db, login_manager, csrf
from models import User
from routes import register_routes
from auth import register_auth_routes

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)

app.secret_key = os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    login_url = url_for('login', next=request.path)
    if request.is_json or request.path in ('/create-checkout-session', '/create-subscription-session'):
        return jsonify({'error': 'login_required', 'login_url': login_url}), 401
    return redirect(login_url)


register_routes(app)
register_auth_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
