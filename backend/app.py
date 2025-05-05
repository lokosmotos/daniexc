# backend/app.py
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables
load_dotenv('../.env')

# Initialize Flask app
app = Flask(__name__)

# Configure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'sslmode': 'require'}
}

db = SQLAlchemy(app)

# Candidate Model
class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    position_applied = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    interview_date = db.Column(db.DateTime)
    interview_notes = db.Column(db.Text)
    resume_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Initialize database
with app.app_context():
    db.create_all()

# API Routes
@app.route('/api/test_db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([{
        'id': c.id,
        'full_name': c.full_name,
        'position': c.position_applied,
        'status': c.status
    } for c in candidates])

@app.route('/api/candidates', methods=['POST'])
def add_candidate():
    data = request.json
    new_candidate = Candidate(
        full_name=data['full_name'],
        position_applied=data['position_applied'],
        branch=data['branch'],
        status='Scheduled',
        resume_url=data.get('resume_url', '')
    )
    db.session.add(new_candidate)
    db.session.commit()
    return jsonify({"message": "Candidate added!", "id": new_candidate.id}), 201

# Web Interface
@app.route('/')
def dashboard():
    candidates = Candidate.query.all()
    stats = {
        'total': len(candidates),
        'hired': len([c for c in candidates if c.status == 'Hired']),
        'scheduled': len([c for c in candidates if c.status == 'Scheduled'])
    }
    return render_template('index.html', candidates=candidates, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
