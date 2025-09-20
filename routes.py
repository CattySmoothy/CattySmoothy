from flask import render_template

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html', title="Home")

    @app.route('/about')
    def about():
        return render_template('about.html', title="About")

    @app.route('/collections')
    def collections():
        return render_template('collections.html', title="Collections")

    @app.route('/profile')
    def profile():
        return render_template('profile.html', title="Profile")
