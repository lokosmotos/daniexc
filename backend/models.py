# backend/models.py
from app import db

class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    position_applied = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'Scheduled', 'Hired', etc.
    interview_date = db.Column(db.DateTime)
    interview_notes = db.Column(db.Text)
    resume_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Candidate {self.full_name}>'
