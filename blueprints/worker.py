import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, Complaint, ProofImage
from utils import role_required, allowed_file, ensure_dirs

worker_bp = Blueprint('worker', __name__, template_folder='../templates/worker')

@worker_bp.route('/tasks')
@login_required
@role_required('worker')
def my_tasks():
    tasks = Complaint.query.filter_by(assigned_to=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('worker/tasks.html', tasks=tasks)

@worker_bp.route('/progress', methods=['POST'])
@login_required
@role_required('worker')
def update_progress():
    complaint_id = request.form.get('complaint_id')
    status = request.form.get('status')
    c = Complaint.query.get_or_404(complaint_id)
    if c.assigned_to != current_user.id:
        flash('Not your task', 'danger')
        return redirect(url_for('worker.my_tasks'))
    c.status = status
    db.session.commit()
    flash('Progress updated', 'success')
    return redirect(url_for('worker.my_tasks'))

@worker_bp.route('/proof', methods=['POST'])
@login_required
@role_required('worker')
def upload_proof():
    complaint_id = request.form.get('complaint_id')
    note = request.form.get('note')
    c = Complaint.query.get_or_404(complaint_id)
    if c.assigned_to != current_user.id:
        flash('Not your task', 'danger')
        return redirect(url_for('worker.my_tasks'))

    ensure_dirs()
    file = request.files.get('proof')
    if file and allowed_file(file.filename):
        fname = secure_filename(file.filename)
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'proofs', f"{complaint_id}_{fname}")
        file.save(path)
        db.session.add(ProofImage(complaint_id=complaint_id, uploader_id=current_user.id, path=path, note=note))
        db.session.commit()
        flash('Proof uploaded', 'success')
    else:
        flash('Invalid file', 'warning')

    return redirect(url_for('worker.my_tasks'))
