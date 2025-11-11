import os
from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import DevConfig
import pymysql
pymysql.install_as_MySQLdb()


login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_object=DevConfig):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    instance_cfg = os.path.join(app.instance_path, 'config.py')
    if os.path.exists(instance_cfg):
        app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    from blueprints.auth import auth_bp
    from blueprints.resident import resident_bp
    from blueprints.admin import admin_bp
    from blueprints.worker import worker_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(resident_bp, url_prefix='/resident')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(worker_bp, url_prefix='/worker')

    @app.route("/")
    def index():
        from flask_login import current_user
        from flask import redirect, url_for, render_template
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.list_complaints'))
            elif current_user.role == 'worker':
                return redirect(url_for('worker.my_tasks'))
            else:
                return redirect(url_for('resident.dashboard'))
        return render_template('base.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
