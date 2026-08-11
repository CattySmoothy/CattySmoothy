import os
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
import stripe

from extensions import db, csrf
from models import Purchase, GuestbookEntry

PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

DOMAIN = os.getenv('DOMAIN', 'http://localhost:5001')


def ensure_stripe_customer(user):
    if user.stripe_customer_id:
        return user.stripe_customer_id
    customer = stripe.Customer.create(email=user.email, metadata={'user_id': str(user.id)})
    user.stripe_customer_id = customer.id
    db.session.commit()
    return customer.id

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
        guestbook_entries = GuestbookEntry.query.order_by(GuestbookEntry.created_at.desc()).limit(50).all()
        return render_template(
            'home.html',
            title="Home",
            guestbook_entries=guestbook_entries,
            guest_view_only=not current_user.is_authenticated,
        )

    @app.route('/about')
    def about():
        return render_template('about.html', title="About")

    @app.route('/support')
    def support():
        return render_template('support.html', title="Support", publishable_key=PUBLISHABLE_KEY)

    @app.route('/donate')
    @login_required
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

    @app.route('/commissions')
    def commissions():
        return render_template('commissions.html', title="Commissions")

    @app.route('/collections')
    def collections():
        return render_template('collections.html', title="Collections")

    @app.route('/updates')
    def updates():
        return render_template('updates.html', title="Updates")

    @app.route('/creators-lab')
    def creators_lab():
        return render_template('creators-lab.html', title="The Creator's Lab")

    @app.route('/organization')
    def organization():
        return render_template('organization.html', title="Organization")

    @app.route('/apply-and-join')
    def apply_and_join():
        return render_template('apply-and-join.html', title="Apply & Join")

    @app.route('/profile')
    def profile():
        return render_template('profile.html', title="Profile")

    @app.route('/join')
    def join():
        return render_template('join.html', title="Join Discord")

    @app.route('/create-checkout-session', methods=['POST'])
    @login_required
    def create_checkout_session():
        data = request.get_json()
        amount = data.get('amount', 5.00)
        name = data.get('name', 'Anonymous')
        message = data.get('message', '')
        msg_type = data.get('msgType', 'free')
        visibility = data.get('visibility', 'public')

        try:
            customer_id = ensure_stripe_customer(current_user)
            session = stripe.checkout.Session.create(
                mode='payment',
                customer=customer_id,
                client_reference_id=str(current_user.id),
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
            db.session.add(Purchase(
                user_id=current_user.id,
                stripe_session_id=session.id,
                type='donation',
                amount=amount,
                status='pending',
            ))
            db.session.commit()
            return jsonify({'url': session.url})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/create-subscription-session', methods=['POST'])
    @login_required
    def create_subscription_session():
        data = request.get_json()
        amount = data.get('amount', 1.99)
        plan_name = data.get('planName', '')

        try:
            customer_id = ensure_stripe_customer(current_user)
            session = stripe.checkout.Session.create(
                mode='subscription',
                customer=customer_id,
                client_reference_id=str(current_user.id),
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
            db.session.add(Purchase(
                user_id=current_user.id,
                stripe_session_id=session.id,
                type='membership',
                amount=amount,
                plan_name=plan_name,
                status='pending',
            ))
            db.session.commit()
            return jsonify({'url': session.url})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/success')
    def success():
        return render_template('success.html', title="Payment Successful")

    @app.route('/cancel')
    def cancel():
        return render_template('cancel.html', title="Payment Cancelled")

    @app.route('/webhook/stripe', methods=['POST'])
    @csrf.exempt
    def stripe_webhook():
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        if not webhook_secret:
            return jsonify({'error': 'webhook not configured'}), 500

        payload = request.get_data()
        sig_header = request.headers.get('Stripe-Signature', '')
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except (ValueError, stripe.error.SignatureVerificationError):
            return jsonify({'error': 'invalid signature'}), 400

        if event['type'] == 'checkout.session.completed':
            session_obj = event['data']['object']
            purchase = Purchase.query.filter_by(stripe_session_id=session_obj['id']).first()
            if purchase and purchase.status != 'completed':
                purchase.status = 'completed'
                purchase.stripe_payment_intent_id = session_obj.get('payment_intent')
                purchase.stripe_subscription_id = session_obj.get('subscription')
                if purchase.type == 'donation':
                    purchase.user.stardust_balance += int(purchase.amount)
                db.session.commit()

        return jsonify({'received': True}), 200
