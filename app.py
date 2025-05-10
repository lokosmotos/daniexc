from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(150), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    resume_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='New Application')
    status_reason = db.Column(db.String(500), nullable=True)
    date_iv = db.Column(db.DateTime, nullable=True)
    date_training = db.Column(db.Date, nullable=True)
    offer_letter = db.Column(db.String(150), nullable=True)
    ic = db.Column(db.String(150), nullable=True)
    candidate_form = db.Column(db.String(150), nullable=True)
    nda = db.Column(db.String(150), nullable=True)
    hostel_required = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_user():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('password123', method='sha256')
        new_user = User(username='admin', password=hashed_password, role='HR')
        db.session.add(new_user)
        db.session.commit()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'HR':
        # Initialize all possible statuses
        all_statuses = [
            'New Application',
            'Interview Scheduled',
            'Practical Test Scheduled',
            'Offer Sent',
            'Hired',
            'KIV',
            'Rejected',
            'WL',
            'Withdraw'
        ]

        today = datetime.today().date()
        today_interviews = Candidate.query.filter(
            Candidate.status == 'Interview Scheduled',
            func.date(Candidate.date_iv) == today
        ).all()

        # Get status counts
        status_counts = defaultdict(int)
        counts = db.session.query(
            Candidate.status,
            func.count(Candidate.id)
        ).group_by(Candidate.status).all()
        
        for status, count in counts:
            status_counts[status] = count
        
        # Ensure all statuses are represented
        for status in all_statuses:
            if status not in status_counts:
                status_counts[status] = 0
        
        candidates = Candidate.query.order_by(Candidate.date_created.desc()).all()
        
        return render_template('dashboard.html',
                           user=current_user,
                           candidates=candidates,
                           status_counts=dict(status_counts),
                           current_date=datetime.now().strftime('%Y-%m-%d'),
                           today_interviews=today_interviews)
    else:
        flash('Access denied.')
        return redirect(url_for('login'))

@app.route('/schedule_interview', methods=['POST'])
def schedule_interview():
    candidate_id = request.form.get('candidate_id')
    interview_date = request.form.get('interview_date')
    interview_time = request.form.get('interview_time')
    
    # Combine date and time and update candidate record
    candidate = Candidate.query.get(candidate_id)
    if candidate:
        candidate.date_iv = datetime.strptime(
            f"{interview_date} {interview_time}", 
            "%Y-%m-%d %H:%M"
        )
        db.session.commit()
        flash('Interview scheduled successfully', 'success')
    else:
        flash('Candidate not found', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/bulk_schedule_interviews', methods=['POST'])
def bulk_schedule_interviews():
    candidate_ids = request.form.getlist('candidate_ids')
    interview_date = request.form.get('interview_date')
    interview_time = request.form.get('interview_time')
    
    # Process each selected candidate
    for candidate_id in candidate_ids:
        candidate = Candidate.query.get(candidate_id)
        if candidate:
            candidate.date_iv = datetime.strptime(
                f"{interview_date} {interview_time}", 
                "%Y-%m-%d %H:%M"
            )
    
    db.session.commit()
    flash(f'Scheduled {len(candidate_ids)} interviews', 'success')
    return redirect(url_for('dashboard'))

@app.route('/add_candidate', methods=['GET', 'POST'])
@login_required
def add_candidate():
    if current_user.role != 'HR':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Get all form data with defaults for optional fields
            name = request.form.get('name', '').strip()
            age = int(request.form.get('age', 0))
            position = request.form.get('position', '').strip()
            branch = request.form.get('branch', 'HQ').strip()
            phone_number = request.form.get('phone_number', '').strip()
            email = request.form.get('email', '').strip().lower()
            status = request.form.get('status', 'New Application').strip()
            
            # Handle file uploads
            resume_url = request.form.get('resume_url', '').strip()
            offer_letter = request.form.get('offer_letter', '').strip()
            ic = request.form.get('ic', '').strip()
            candidate_form = request.form.get('candidate_form', '').strip()
            nda = request.form.get('nda', '').strip()
            
            # Handle dates
            date_iv = request.form.get('date_iv')
            date_training = request.form.get('date_training')
            
            # Convert dates from string to date objects
            date_iv = datetime.strptime(date_iv, '%Y-%m-%d').date() if date_iv else None
            date_training = datetime.strptime(date_training, '%Y-%m-%d').date() if date_training else None
            
            # Determine hostel requirement
            hostel_required = branch in ['JB', 'DP', 'SA']
            
            # Handle status reason
            status_reason = request.form.get('status_reason', '').strip()
            if status not in ['Rejected', 'KIV', 'Withdraw']:
                status_reason = None
            
            # Create new candidate
            new_candidate = Candidate(
                name=name,
                age=age,
                position=position,
                branch=branch,
                phone_number=phone_number,
                email=email,
                resume_url=resume_url,
                status=status,
                status_reason=status_reason,
                date_iv=date_iv,
                date_training=date_training,
                offer_letter=offer_letter,
                ic=ic,
                candidate_form=candidate_form,
                nda=nda,
                hostel_required=hostel_required
            )
            
            db.session.add(new_candidate)
            db.session.commit()
            
            flash('Candidate added successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Invalid data format: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding candidate: {str(e)}', 'danger')
    
    # For GET request or if POST fails
    return render_template('add_candidate.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone_number')  # Changed to match your model
            position = request.form.get('position')
            
            # Handle file upload
            resume = request.files.get('resume')
            resume_url = None
            if resume and allowed_file(resume.filename):
                filename = secure_filename(resume.filename)
                resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                resume_url = filename  # Or full path if needed
            
            # Create new candidate - match your model fields
            new_candidate = Candidate(
                name=name,
                email=email,
                phone_number=phone,  # Match model field name
                position=position,
                resume_url=resume_url,  # Match model field name
                status='New Application',
                branch='HQ',  # Set default or get from form
                age=0,  # Set default or add to form
                hostel_required=False  # Set default or add to form
            )
            
            db.session.add(new_candidate)
            db.session.commit()
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('apply'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting application: {str(e)}', 'danger')
    
    return render_template('apply.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}

@app.route('/update_status/<int:candidate_id>', methods=['POST'])
@login_required
def update_status(candidate_id):
    if current_user.role == 'HR':
        candidate = Candidate.query.get_or_404(candidate_id)
        new_status = request.form.get('status')
        status_reason = request.form.get('status_reason', None)
        
        candidate.status = new_status
        if new_status in ['Rejected', 'KIV', 'Withdraw']:
            candidate.status_reason = status_reason
        else:
            candidate.status_reason = None
        
        db.session.commit()
        flash('Status updated successfully!')
        return redirect(url_for('dashboard'))
    else:
        flash('Access denied.')
        return redirect(url_for('login'))

@app.route('/view_candidate/<int:candidate_id>')
@login_required
def view_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('view_candidate.html', candidate=candidate)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
