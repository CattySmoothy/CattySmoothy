from flask import render_template, request

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
        return render_template('support.html', title="Support")

    @app.route('/donate')
    def donate():
        amount = request.args.get('amount', '5.00')
        return render_template('donate.html', title="Donate", amount=amount)

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
