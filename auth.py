from urllib.parse import urlparse

from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User, Purchase
from forms import RegisterForm, LoginForm


def _is_safe_next(target):
    if not target:
        return False
    ref = urlparse(target)
    return ref.netloc == '' and target.startswith('/')


def register_auth_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if request.method == 'GET':
            return render_template('register.html', title="Register", next=request.args.get('next', ''))

        payload = request.get_json(silent=True) or {}
        form = RegisterForm(data=payload)
        if not form.validate():
            return jsonify({'error': next(iter(form.errors.values()))[0]}), 400

        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'An account with that email already exists.'}), 400

        user = User(email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        next_url = request.args.get('next') or payload.get('next')
        return jsonify({'redirect': next_url if _is_safe_next(next_url) else url_for('home')})

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if request.method == 'GET':
            return render_template('login.html', title="Log In", next=request.args.get('next', ''))

        payload = request.get_json(silent=True) or {}
        form = LoginForm(data=payload)
        if not form.validate():
            return jsonify({'error': 'Please enter a valid email and password.'}), 400

        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(form.password.data):
            return jsonify({'error': 'Invalid email or password.'}), 401

        login_user(user)
        next_url = request.args.get('next') or payload.get('next')
        return jsonify({'redirect': next_url if _is_safe_next(next_url) else url_for('home')})

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/account')
    @login_required
    def account():
        purchases = current_user.purchases.order_by(Purchase.created_at.desc()).all()
        return render_template('account.html', title="Account", purchases=purchases)
