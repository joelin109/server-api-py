from src.webhttp.blueprint import register_blueprint
from src.webhttp.extension_admin import register_admin
from src.webhttp.extension_login import register_login


def register_extension(app):
    register_blueprint(app)
    register_admin(app)
    register_login(app)
