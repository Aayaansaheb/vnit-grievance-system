import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, Complaint, ComplaintImage, STATUS_PENDING, PRIORITY_EMERGENCY
from utils import allowed_file, detect_emergency, role_required, ensure_dirs

resident_bp = Blueprint('resident', __name__, template_folder='../templates/resident')

@resident_bp.route('/dashboard')
@login_required
@role_required('resident')
def dashboard():
    complaints = Complaint.query.filter_by(resident_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('resident/dashboard.html', complaints=complaints)

@resident_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('resident')
def new_complaint():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        hostel = request.form.get('hostel') or current_user.hostel
        room = request.form.get('room') or current_user.room

        priority = PRIORITY_EMERGENCY if detect_emergency(f"{title} {description}") else 'Normal'

        c = Complaint(
            resident_id=current_user.id,
            title=title,
            category=category,
            description=description,
            hostel=hostel,
            room=room,
            priority=priority,
            status=STATUS_PENDING
        )
        db.session.add(c)
        db.session.commit()

        ensure_dirs()
        files = request.files.getlist('images')
        for f in files:
            if f and allowed_file(f.filename):
                fname = secure_filename(f.filename)
                save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'complaints', f"{c.id}_{fname}")
                f.save(save_path)
                db.session.add(ComplaintImage(complaint_id=c.id, path=save_path))
        db.session.commit()

        flash('Complaint submitted!', 'success')
        return redirect(url_for('resident.dashboard'))

    return render_template('resident/complaint.html')
