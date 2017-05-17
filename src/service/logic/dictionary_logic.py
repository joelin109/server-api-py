from datetime import datetime
from src.service.model.connection import conn, execute_total
from src.service.logic.util_logic import UtilLogic, ListFilter
from src.service.model.model_content import ContentDictionary
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.expression import or_
from sqlalchemy import desc
from src.service.util.logger import *
import traceback


class DictionaryLogic(UtilLogic):
    def new(self, new_wort):
        self._verify_except_case()

        conn.add(new_wort)
        conn.commit()
        return True

    def update(self, new_wort):
        self._verify_except_case()

        conn.query(ContentDictionary).filter_by(id=new_wort.id).update({
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
            ContentDictionary.last_update_date: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        conn.commit()
        return True

    def delete(self, wort):
        self._verify_except_case()

        conn.delete(wort)
        conn.commit()
        return True

    # SECtable.date.endswith(matchingString) str(ContentDictionary.wort)[:1] == str("a")
    def get_list(self, list_filter=None):
        try:
            if list_filter is None:
                list_filter = WordListFilter()

            _filter_sql = list_filter.filter_sql + " ORDER BY lower(wort) " + list_filter.offset_limit_sql
            # print(_filter_sql)
            # _listResult = session.execute("select * from content_dictionary_de limit 10", mapper=ContentDictionary)
            _listResult = conn.query(ContentDictionary).filter(_filter_sql)
            _total = execute_total(ContentDictionary.__tablename__, list_filter.filter_sql)

        except Exception as ex:
            print('get_list except Exception as ex')
            raise RuntimeError(ex)

        # for row in _listResult:
        #    for s in inspect(ContentDictionary).attrs.keys():
        #        if s in row:
        #            print(row)

        return self.new_result_page(_listResult, list_filter, _total)

    def get_detail(self, word_id):
        self._verify_except_case()

        _word = conn.query(ContentDictionary).filter_by(wort=word_id).first()
        return _word


class WordListFilter(ListFilter):
    is_regel = -1
    word_letter = ""
    word_sex = ""
    word_type = ""

    def parse(self, data_filter=None):
        self.base_parse(data_filter)

        self.word_letter = data_filter["letter"]

        _filter_letter = 'lower(substring(wort, 1, 1)) = \'%s\' ' % self.word_letter.lower()
        self.filter_sql = '1=1' if self.word_letter == '' else _filter_letter