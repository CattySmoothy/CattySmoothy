import os
from flask import Flask
from dotenv import load_dotenv
import stripe
from routes import register_routes

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)