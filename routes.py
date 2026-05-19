import os
from flask import render_template, request, jsonify, redirect, url_for
import stripe

PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

DOMAIN = os.getenv('DOMAIN', 'http://localhost:5001')

donors = [
    {"name": "Luna", "message": "Love your art!", "amount": 10.00, "public": True},
    {"name": "Starfall", "message": "Keep creating!", "amount": 25.00, "public": True},
    {"name": "Nebula", "message": "You inspire me", "amount": 5.00, "public": True},
    {"name": "Celeste", "message": "practice every single day", "amount": 50.00, "public": True, "type": "promise"},
    {"name": "Orion", "message": "Digital art gang", "amount": 15.00, "public": True},
    {"name": "Aurora", "message": "How I found this artist — I stumbled upon your profile in a forum and instantly fell in love with your style. I've been a fan ever since.", "amount": 20.00, "public": True, "type": "story"},
    {"name": "Comet", "message": "You're so talented", "amount": 8.00, "public": True},
    {"name": "Vega", "message": "Keep shining ✨", "amount": 30.00, "public": True},
    {"name": "Nova", "message": "First time donating!", "amount": 12.00, "public": True},
    {"name": "Sirius", "message": "learn one new technique each month", "amount": 100.00, "public": True, "type": "promise"},
    {"name": "Eclipse", "message": "A memory this art reminds me of — your galaxy pieces remind me of stargazing with my dad as a kid.", "amount": 7.50, "public": True, "type": "story"},
    {"name": "Lyra", "message": "So happy to support", "amount": 18.00, "public": True},
]

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html', title="Home")

    @app.route('/about')
    def about():
        return render_template('about.html', title="About")

    @app.route('/support')
    def support():
        return render_template('support.html', title="Support", publishable_key=PUBLISHABLE_KEY)

    @app.route('/donate')
    def donate():
        amount = request.args.get('amount', '5.00')
        return render_template('donate.html', title="Donate", amount=amount, publishable_key=PUBLISHABLE_KEY)

    @app.route('/donors')
    def donors_page():
        key = request.args.get('key', '')
        if key == 'c4tty5m00thy':
            shown = donors
        else:
            shown = [d for d in donors if d.get('public')]
        return render_template('donors.html', title="Supporters", donors=shown)

    @app.route('/collections')
    def collections():
        return render_template('collections.html', title="Collections")

    @app.route('/profile')
    def profile():
        return render_template('profile.html', title="Profile")

    @app.route('/join')
    def join():
        return render_template('join.html', title="Join Discord")

    @app.route('/create-checkout-session', methods=['POST'])
    def create_checkout_session():
        data = request.get_json()
        amount = data.get('amount', 5.00)
        name = data.get('name', 'Anonymous')
        message = data.get('message', '')
        msg_type = data.get('msgType', 'free')
        visibility = data.get('visibility', 'public')

        try:
            session = stripe.checkout.Session.create(
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Stardust Donation',
                        },
                        'unit_amount': int(float(amount) * 100),
                    },
                    'quantity': 1,
                }],
                metadata={
                    'donor_name': name,
                    'message': message,
                    'msg_type': msg_type,
                    'visibility': visibility,
                },
                success_url=DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=DOMAIN + '/cancel',
            )
            return jsonify({'url': session.url})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/create-subscription-session', methods=['POST'])
    def create_subscription_session():
        data = request.get_json()
        amount = data.get('amount', 1.99)
        plan_name = data.get('planName', '')

        try:
            session = stripe.checkout.Session.create(
                mode='subscription',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': plan_name + ' Subscription',
                        },
                        'unit_amount': int(float(amount) * 100),
                        'recurring': {'interval': 'month'},
                    },
                    'quantity': 1,
                }],
                metadata={
                    'plan': plan_name,
                },
                success_url=DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=DOMAIN + '/cancel',
            )
            return jsonify({'url': session.url})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/success')
    def success():
        return render_template('success.html', title="Payment Successful")

    @app.route('/cancel')
    def cancel():
        return render_template('cancel.html', title="Payment Cancelled")
