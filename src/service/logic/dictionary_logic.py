from src.service.model.model_content import db, ContentDictionary
from src.service.logic.util_logic import UtilLogic
from datetime import datetime
from sqlalchemy.sql.expression import or_
from sqlalchemy import desc
from src.service.util.logger import *
import traceback


class DictionaryLogic(UtilLogic):
    def new(self, new_wort):
        self._verify_except_case()

        db.session.add(new_wort)
        db.session.commit()
        return True

    def update_word(self, new_wort):
        self._verify_except_case()

        ContentDictionary.query.filter_by(id=new_wort.id).update({
            ContentDictionary.wort_sex: new_wort.wort_sex,
            ContentDictionary.level: new_wort.level,
            ContentDictionary.type: new_wort.type,
            ContentDictionary.plural: new_wort.plural,
            ContentDictionary.synonym: new_wort.synonym,
            ContentDictionary.wort_zh: new_wort.wort_zh,
            ContentDictionary.wort_en: new_wort.wort_en,
            ContentDictionary.konjugation: new_wort.konjugation,
            ContentDictionary.is_regel: new_wort.is_regel,
            ContentDictionary.is_recommend: new_wort.is_recommend,
            ContentDictionary.update_date: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        db.session.commit()
        return True

    def get_list(self, word_filter=None):
        # .filter_by(is_regel=0)
        try:
            _filter = ''
            if word_filter is None:
                _filter = "1=1 ORDER BY lower(wort)"
            else:
                # SECtable.date.endswith(matchingString) str(ContentDictionary.wort)[:1] == str("a")
                _filter = "lower(SUBSTRING(wort, 1, 1)) = '%s' ORDER BY lower(wort)" % word_filter.word_channel.lower()

            _wordPage = ContentDictionary.query.filter(_filter).paginate(1, 200, False)

        except Exception as ex:
            raise RuntimeError(ex)

        return self.result_page(_wordPage)

    def get_detail(self, word_id):
        self._verify_except_case()

        _word = ContentDictionary.query.filter_by(wort=word_id).first()
        return _word


class WordFilter:
    page = 1
    is_recommend = -1
    is_regel = -1
    word_channel = ""
    word_sex = ""
    word_type = ""

    def parse(self, filters=None):
        self.is_recommend = 1
        # self.word_type = filters["type"]
        # self.word_sex = filters["sex"]
        self.word_channel = filters["channel"]
