from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Raichuu</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 1rem;
        }
        nav {
            background-color: #444;
            color: #fff;
            padding: 0.5rem;
        }
        nav a {
            color: #fff;
            text-decoration: none;
            padding: 0.5rem;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
            padding: 20px;
        }
        .btn {
            display: inline-block;
            background: #333;
            color: #fff;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Raichuu</h1>
        <p>Creating digital art, process videos, tutorials, wallpapers and more</p>
    </header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/collections">Collections</a>
    </nav>
    <div class="container">
        <h2>{{ title }}</h2>
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <p>Welcome to my personal art platform!</p>
    <p>29,499 members • 166 Posts</p>
    <a href="#" class="btn">Join for free</a>
    <div>
        <a href="#"><img src="path_to_instagram_icon.png" alt="Instagram"></a>
        <a href="#"><img src="path_to_youtube_icon.png" alt="YouTube"></a>
        <a href="#"><img src="path_to_twitter_icon.png" alt="Twitter"></a>
    </div>
    """
    return render_template_string(html_template, title="Home", content=content)

@app.route('/about')
def about():
    content = """
    <p>Hello! My name is Sam! I'm a 25yo digital artist based in Toronto. I love to paint! Art has actually been a passion of mine for most of my life! I stopped learning art after high school, kept it as a side hobby but I didn't make any real attempts to improve and get better. But early 2020 I decided to take it seriously and here we are!</p>
    """
    return render_template_string(html_template, title="About", content=content)

@app.route('/collections')
def collections():
    content = """
    <h3>My Art Collections</h3>
    <ul>
        <li>Digital Paintings</li>
        <li>Process Videos</li>
        <li>Tutorials</li>
        <li>Wallpapers</li>
        <li>Sketches</li>
    </ul>
    """
    return render_template_string(html_template, title="Collections", content=content)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
