from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import pymysql
from src.service.config import SQLConfig


class DataBase:
    uri = SQLConfig.SQLALCHEMY_DATABASE_URI

    def engine(self):
        return create_engine(self.uri, echo=False)

    def connection(self):
        print('connection - create_engine')
        _engine = self.engine()
        _Session = sessionmaker(bind=_engine)  # 将创建的数据库连接关联到这个session
        return _Session()


def register_db_connection(app):
    _uri = DataBase().uri
    database_uri = _uri.split(":")[0]
    if database_uri == 'mysql':
        pymysql.install_as_MySQLdb()
    else:
        print(database_uri)

# connection ~ = db.session (db = db = SQLAlchemy())
connection = DataBase().connection()


def execute_total(table, filter_sql=None):
    _filter_sql = "" if filter_sql is None else " where " + filter_sql
    _count_sql = "select count(*) from " + table + _filter_sql
    _listCount = connection.execute(_count_sql)

    _total = 0
    for c in _listCount:
        _total = c.count

    return _total
