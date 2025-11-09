from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

ROLE_RESIDENT = "resident"
ROLE_ADMIN = "admin"
ROLE_WORKER = "worker"

STATUS_PENDING = "Pending"
STATUS_IN_PROGRESS = "In Progress"
STATUS_COMPLETED = "Completed"
STATUS_RESOLVED = "Resolved"
STATUS_REJECTED = "Rejected"

PRIORITY_NORMAL = "Normal"
PRIORITY_EMERGENCY = "Emergency"

ALLOWED_STATUSES = [
    STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_RESOLVED, STATUS_REJECTED
]

ALLOWED_PRIORITIES = [PRIORITY_NORMAL, PRIORITY_EMERGENCY]

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=ROLE_RESIDENT)
    hostel = db.Column(db.String(120))
    room = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaints = db.relationship("Complaint", backref="resident", lazy=True, foreign_keys="Complaint.resident_id")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    hostel = db.Column(db.String(120))
    room = db.Column(db.String(20))
    priority = db.Column(db.String(20), default=PRIORITY_NORMAL)
    status = db.Column(db.String(20), default=STATUS_PENDING)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship("ComplaintImage", backref="complaint", lazy=True, cascade="all,delete-orphan")
    proofs = db.relationship("ProofImage", backref="complaint", lazy=True, cascade="all,delete-orphan")

class ComplaintImage(db.Model):
    __tablename__ = "complaint_images"

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey("complaints.id"), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProofImage(db.Model):
    __tablename__ = "proof_images"

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey("complaints.id"), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
