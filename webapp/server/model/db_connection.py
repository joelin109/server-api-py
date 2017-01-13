from flask_sqlalchemy import SQLAlchemy
import pymysql
from webapp.server.config import SQLConfig


def mysql_db_connection(uri):
    database_uri = uri.split(":")[0]
    if database_uri == 'mysql':
        pymysql.install_as_MySQLdb()
    else:
        print(database_uri)


def register_db_connection(app):
    app.config.from_object(SQLConfig)
    db.init_app(app)


mysql_db_connection(SQLConfig.SQLALCHEMY_DATABASE_URI)
"""
app = Flask(__name__)
db = SQLAlchemy(app)
"""
db = SQLAlchemy()
