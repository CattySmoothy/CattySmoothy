from flask import render_template

donors = [
    {"name": "Luna", "message": "Love your art!", "amount": 10.00},
    {"name": "Starfall", "message": "Keep creating!", "amount": 25.00},
    {"name": "Nebula", "message": "You inspire me", "amount": 5.00},
    {"name": "Celeste", "message": "Amazing work!", "amount": 50.00},
    {"name": "Orion", "message": "Digital art gang", "amount": 15.00},
    {"name": "Aurora", "message": "More tutorials please!", "amount": 20.00},
    {"name": "Comet", "message": "You're so talented", "amount": 8.00},
    {"name": "Vega", "message": "Keep shining ✨", "amount": 30.00},
    {"name": "Nova", "message": "First time donating!", "amount": 12.00},
    {"name": "Sirius", "message": "Best artist ever", "amount": 100.00},
    {"name": "Eclipse", "message": "Love the style", "amount": 7.50},
    {"name": "Lyra", "message": "So happy to support", "amount": 18.00},
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

    @app.route('/donors')
    def donors_page():
        return render_template('donors.html', title="Supporters", donors=donors)

    @app.route('/collections')
    def collections():
        return render_template('collections.html', title="Collections")

    @app.route('/profile')
    def profile():
        return render_template('profile.html', title="Profile")

    @app.route('/join')
    def join():
        return render_template('join.html', title="Join Discord")
