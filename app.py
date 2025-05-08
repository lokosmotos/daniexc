from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    status = db.Column(db.String(50), nullable=False)
    date_iv = db.Column(db.Date, nullable=True)
    date_training = db.Column(db.Date, nullable=True)
    offer_letter = db.Column(db.String(150), nullable=True)
    ic = db.Column(db.String(150), nullable=True)
    candidate_form = db.Column(db.String(150), nullable=True)
    nda = db.Column(db.String(150), nullable=True)
    hostel_required = db.Column(db.Boolean, nullable=False, default=False)


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
        candidates = Candidate.query.all()  # Retrieve all candidates
        return render_template('dashboard.html', user=current_user, candidates=candidates)
    else:
        flash('Access denied.')
        return redirect(url_for('login'))


@app.route('/add_candidate', methods=['GET', 'POST'])
@login_required
def add_candidate():
    if current_user.role == 'HR':  # Allow HR to add candidates
        if request.method == 'POST':
            name = request.form.get('name')
            age = request.form.get('age')
            position = request.form.get('position')
            branch = request.form.get('branch')
            phone_number = request.form.get('phone_number')
            email = request.form.get('email')
            resume_url = request.form.get('resume_url')
            status = request.form.get('status')
            date_iv = request.form.get('date_iv')
            date_training = request.form.get('date_training')
            offer_letter = request.form.get('offer_letter')
            ic = request.form.get('ic')
            candidate_form = request.form.get('candidate_form')
            nda = request.form.get('nda')
            hostel_required = True if branch in ['JB', 'DP', 'SA'] else False

            new_candidate = Candidate(
                name=name,
                age=age,
                position=position,
                branch=branch,
                phone_number=phone_number,
                email=email,
                resume_url=resume_url,
                status=status,
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
            flash('Candidate added successfully!')
            return redirect(url_for('dashboard'))
        
        return render_template('add_candidate.html')
    else:
        flash('Access denied.')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
