from sqlalchemy.inspection import inspect
from datetime import datetime
from webapp.server.model.db_connection import db


def serialize(self):
    return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
