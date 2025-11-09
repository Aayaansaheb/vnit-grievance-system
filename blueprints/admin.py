from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, User, Complaint, ALLOWED_STATUSES
from utils import role_required

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

@admin_bp.route('/complaints')
@login_required
@role_required('admin')
def list_complaints():
    q = Complaint.query
    status = request.args.get('status')
    category = request.args.get('category')
    priority = request.args.get('priority')
    if status:
        q = q.filter_by(status=status)
    if category:
        q = q.filter_by(category=category)
    if priority:
        q = q.filter_by(priority=priority)
    complaints = q.order_by(Complaint.priority.desc(), Complaint.created_at.desc()).all()

    workers = User.query.filter_by(role='worker').all()
    return render_template('admin/complaints.html', complaints=complaints, workers=workers, statuses=ALLOWED_STATUSES)

@admin_bp.route('/assign', methods=['POST'])
@login_required
@role_required('admin')
def assign_worker():
    complaint_id = request.form.get('complaint_id')
    worker_id = request.form.get('worker_id')
    c = Complaint.query.get_or_404(complaint_id)
    c.assigned_to = int(worker_id) if worker_id else None
    db.session.commit()
    flash('Assigned!', 'success')
    return redirect(url_for('admin.list_complaints'))

@admin_bp.route('/status', methods=['POST'])
@login_required
@role_required('admin')
def update_status():
    complaint_id = request.form.get('complaint_id')
    status = request.form.get('status')
    c = Complaint.query.get_or_404(complaint_id)
    if status in ALLOWED_STATUSES:
        c.status = status
        db.session.commit()
        flash('Status updated', 'success')
    else:
        flash('Invalid status', 'danger')
    return redirect(url_for('admin.list_complaints'))
