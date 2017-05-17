from src.service.model.db_connection import DataBase
from src.service.model.model_content import *


class Model:
    db = DataBase()

    def create_all(self):
        _engine = self.db.engine()
        # _base_model = declarative_base()
        # _base_model.metadata.create_all(bind=_engine)
        ContentLike.__table__.create(_engine, checkfirst=True)
        ContentStatisticArticle.__table__.create(_engine, checkfirst=True)
        content_relation_tag.create(_engine, checkfirst=True)
        content_relation_account.create(_engine, checkfirst=True)
