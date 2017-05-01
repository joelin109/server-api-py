from flask_sqlalchemy import SQLAlchemy
import pymysql
from src.service.config import SQLConfig

from datetime import datetime
from base64 import b64encode
from os import urandom


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


def custom_random_key(self, table_tag=None):
    random_bytes = urandom(18)
    _key = datetime.now().strftime('%y%m') + b64encode(random_bytes).decode('utf-8')
    _key = _key if table_tag is None else table_tag + _key

    _key_32 = _key if len(_key) <= 32 else _key[0:32]
    return _key_32
