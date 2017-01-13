from flask_login import LoginManager
from flask_principal import Permission, RoleNeed
from flask_admin import Admin

f_admin = Admin()

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from webapp.server.model.model_account import User
    return User.query.get(user_id)
