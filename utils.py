import os
from functools import wraps
from flask import current_app, abort
from flask_login import current_user

EMERGENCY_KEYWORDS = {
    "fire", "smoke", "gas leak", "leak", "water leakage", "water leak",
    "short circuit", "sparks", "electrocution", "medical", "unconscious",
    "bleeding", "faint", "power outage", "power cut","intruder",
}

def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator

def allowed_file(filename: str) -> bool:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in current_app.config.get("ALLOWED_EXTENSIONS", set())

def detect_emergency(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in EMERGENCY_KEYWORDS)

def ensure_dirs():
    base = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(os.path.join(base, "complaints"), exist_ok=True)
    os.makedirs(os.path.join(base, "proofs"), exist_ok=True)
