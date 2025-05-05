# backend/routes/candidates.py
from flask import Blueprint, request, jsonify
from models import Candidate, db

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([{
        'id': c.id,
        'full_name': c.full_name,
        'position_applied': c.position_applied,
        'status': c.status
    } for c in candidates])

@candidates_bp.route('/candidates', methods=['POST'])
def add_candidate():
    data = request.json
    new_candidate = Candidate(
        full_name=data['full_name'],
        age=data.get('age'),
        contact_number=data.get('contact_number'),
        email=data.get('email'),
        position_applied=data['position_applied'],
        branch=data['branch'],
        status=data['status'],
        interview_date=data.get('interview_date'),
        resume_url=data.get('resume_url')
    )
    db.session.add(new_candidate)
    db.session.commit()
    return jsonify({"message": "Candidate added!", "id": new_candidate.id}), 201
