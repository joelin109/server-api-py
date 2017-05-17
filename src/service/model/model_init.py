from src.service.model.connection import DataBase
from src.service.model.model_account import *
from src.service.model.model_content import *


class Model:
    db = DataBase()

    def create_all(self):
        _engine = self.db.engine()

        User.__table__.create(_engine, checkfirst=True)
        UserAuthToken.__table__.create(_engine, checkfirst=True)

        ContentChannel.__table__.create(_engine, checkfirst=True)
        ContentTag.__table__.create(_engine, checkfirst=True)
        ContentArticle.__table__.create(_engine, checkfirst=True)
        ContentDictionary.__table__.create(_engine, checkfirst=True)
        ContentComment.__table__.create(_engine, checkfirst=True)
        ContentLike.__table__.create(_engine, checkfirst=True)
        ContentStatisticArticle.__table__.create(_engine, checkfirst=True)

        content_relation_tag.create(_engine, checkfirst=True)
        content_relation_account.create(_engine, checkfirst=True)
