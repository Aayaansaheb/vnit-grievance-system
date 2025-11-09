from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User, ROLE_RESIDENT, ROLE_ADMIN, ROLE_WORKER

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        flash('Invalid credentials', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hostel = request.form.get('hostel')
        room = request.form.get('room')
        role = request.form.get('role', ROLE_RESIDENT)
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('auth.register'))
        u = User(name=name, email=email, hostel=hostel, room=room, role=role)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash('Registered! You can login now.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', roles=[ROLE_RESIDENT, ROLE_WORKER, ROLE_ADMIN])

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
