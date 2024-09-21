from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html', title="Home")

@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/collections')
def collections():
    return render_template('collections.html', title="Collections")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
