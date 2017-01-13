from webapp.server.model.model_content import db, ContentDictionary
from webapp.server.logic.util_handler import UtilHandler
from datetime import datetime


class DictionaryHandler(UtilHandler):
    def word_list(self, filters=None):
        # .filter_by(is_regel=0)
        _wordPage = ContentDictionary.query.order_by(
            ContentDictionary.wort.asc()
        ).paginate(1, 50, False)

        return self.result_page(_wordPage)

    def word_update(self, new_wort):
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

    def word_new(self, new_wort):
        self._verify_except_case()

        db.session.add(new_wort)
        db.session.commit()
        return True

    def word_detail(self, word_id):
        self._verify_except_case()

        _word = ContentDictionary.query.filter_by(wort=word_id).first()
        return _word
