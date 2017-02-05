from flask_script import Manager, Server
from src.service.model.db_connection import db

from src.main import app

manager = Manager(app)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == "__main__":
    manager.run()
