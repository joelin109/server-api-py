from sqlalchemy.inspection import inspect
from datetime import datetime
from src.service.model.db_connection import db


def serialize(self):
    return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
