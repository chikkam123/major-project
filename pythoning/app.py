'''from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)

# Set the secret key for Flask sessions
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:ssdpm@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate with the app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Login required decorator with role
def login_required(role):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if 'role' not in session or session.get('role') != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapped
    return wrapper

# Home route
@app.route('/')
def home():
    return render_template('home.html')



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for(f'{user.role}_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Register new user route (accessible only by admin)
@app.route('/add_user', methods=['POST'])
@login_required('admin')
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'danger')
    else:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {username} registered successfully as {role}', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin dashboard route
@app.route('/admin_dashboard')
@login_required('admin')
def admin_dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

# Teacher dashboard route
@app.route('/teacher_dashboard',methods=['GET', 'POST'])
@login_required('teacher')
def teacher_dashboard():
    # Sample content for teacher dashboard
    return render_template('teacher_dashboard.html', courses=[])

# Student dashboard route
@app.route('/student_dashboard')
@login_required('student')
def student_dashboard():
    quizzes = []  # Replace with actual quiz retrieval logic
    return render_template('student_dashboard.html', quizzes=quizzes)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@example.com",
                         password=generate_password_hash("adminpass", method='pbkdf2:sha256'),
                         role="admin")
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)'''

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)

# Set the secret key for Flask sessions
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:ssdpm@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate with the app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Login required decorator with role
def login_required(role):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if 'role' not in session or session.get('role') != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapped
    return wrapper

# Context processor to inject user globally
@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'user': user}
    return {'user': None}

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username  # Store username in session
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for(f'{user.role}_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Register new user route (accessible only by admin)
@app.route('/add_user', methods=['POST'])
@login_required('admin')
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'danger')
    else:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {username} registered successfully as {role}', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin dashboard route
@app.route('/admin_dashboard')
@login_required('admin')
def admin_dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

# Teacher dashboard route
@app.route('/teacher_dashboard', methods=['GET', 'POST'])
@login_required('teacher')
def teacher_dashboard():
    return render_template('teacher_dashboard.html', courses=[])


@app.route('/add_quiz', methods=['GET', 'POST'])
@login_required('teacher')
def add_quiz():
    if request.method == 'POST':
        # Logic to handle quiz creation
        quiz_title = request.form.get('quiz_title')
        quiz_description = request.form.get('quiz_description')
        # Add logic to save the quiz to the database
        flash(f'Quiz "{quiz_title}" has been successfully created!', 'success')
        return redirect(url_for('teacher_dashboard'))
    return render_template('add_quiz.html')

# Student dashboard route
@app.route('/student_dashboard')
@login_required('student')
def student_dashboard():
    quizzes = []  # Replace with actual quiz retrieval logic
    return render_template('student_dashboard.html', quizzes=quizzes)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)  # Clear username from session
    session.pop('role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@example.com",
                         password=generate_password_hash("adminpass", method='pbkdf2:sha256'),
                         role="admin")
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)


