from flask_script import Manager, Server
from src.service.model.model_init import Model
from main import app

manager = Manager(app)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    return dict(app=app, db=Model())


if __name__ == "__main__":
    manager.run()


# Step 1: python manage.py shell
# Step 2: db.create_all()

