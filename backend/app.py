# backend/app.py
from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv('../.env')

app = Flask(__name__)

# Configure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import routes (we'll create these next)
from routes.candidates import candidates_bp
app.register_blueprint(candidates_bp)

@app.route('/')
def home():
    return "Hiring App Backend Running!"

if __name__ == '__main__':
    app.run(debug=True)
