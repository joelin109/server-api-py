from src.service.model.connection import conn, execute_total
from src.service.logic.util_logic import UtilLogic, ListFilter
from src.service.model.model_content import ContentArticle
from datetime import datetime
from src.service.util.logger import *


class ArticleLogic(UtilLogic):
    def new(self, new_article):
        self._verify_except_case()

        try:
            conn.add(new_article)
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

        return True

    def update(self, article):
        self._verify_except_case()

        conn.query(ContentArticle).filter_by(id=article.id).update({
            ContentArticle.format_type: article.format_type,
            ContentArticle.body_text: article.body_text,
            ContentArticle.body_match_level: article.body_match_level,
            ContentArticle.publish_status: article.publish_status,
            ContentArticle.is_recommend: article.is_recommend,
            ContentArticle.last_update_date: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        conn.commit()
        return True

    def update_article_status(self, article):
        self._verify_except_case()

        try:
            conn.query(ContentArticle).filter_by(id=article.id).update({
                ContentArticle.publish_status: article.publish_status,
                ContentArticle.is_recommend: article.is_recommend
                # ContentArticle.last_update_date: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            conn.commit()
        except Exception as ex:
            print(str(ex)[0:500])
            conn.rollback()
            self.exec_result = False
        finally:
            conn.close()
            return self.exec_result

    def update_article_body(self, article):
        self._verify_except_case()

        try:
            conn.query(ContentArticle).filter_by(id=article.id).update({
                ContentArticle.title: article.title,
                ContentArticle.is_recommend: article.is_recommend,
                ContentArticle.publish_status: article.publish_status,
                ContentArticle.body_text: article.body_text,
                ContentArticle.body_match_level: article.body_match_level,
                ContentArticle.last_update_date: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            conn.commit()
        except Exception as ex:
            print(str(ex)[0:500])
            conn.rollback()
            self.exec_result = False
        finally:
            conn.close()
            return self.exec_result

    def get_list(self, list_filter=None):
        try:
            if list_filter is None:
                list_filter = ArticleListFilter()

            _filter_sql = list_filter.filter_sql + " order by publish_at desc " + list_filter.offset_limit_sql
            _listResult = conn.query(ContentArticle).filter(_filter_sql)
            _total = execute_total(ContentArticle.__tablename__, list_filter.filter_sql)

        except Exception as ex:
            raise RuntimeError(ex)

        return self.new_result_page(_listResult, list_filter, _total)

    def get_top_list(self, filter_tag_id, filter_date):
        self._verify_except_case()
        try:
            _filter_sql = 'tag_id = \'%s\' AND last_update_date >= \'%s\' limit 100' % (filter_tag_id, filter_date)
            _listResult = conn.query(ContentArticle).filter(_filter_sql)

        except Exception as ex:
            raise RuntimeError(ex)

        _result_row = [m.parse_top() for m in _listResult]
        return _result_row

    def get_detail(self, article_id):
        self._verify_except_case()

        _result = dict()
        _result["id"] = article_id

        try:
            _article = conn.query(ContentArticle).filter_by(id=article_id).first()  # .one()
            _result = _article.parse_detail()
        except Exception as ex:
            print(str(ex)[0:500])
            _result["status"] = False

        return _result


class ArticleListFilter(ListFilter):
    published_at = ""
    publish_status = -1

    def parse(self, data_filter=None):
        self.base_parse(data_filter)

        if 'publish_status' in data_filter:
            self.publish_status = data_filter["publish_status"]
            self.filter_sql += ' AND publish_status = %s' % self.publish_status

        if 'is_recommend' in data_filter:
            self.is_recommend = data_filter["is_recommend"]
            self.filter_sql += ' AND is_recommend = 1' if self.is_recommend == 1 else ''

        if 'published_at' in data_filter:
            self.published_at = data_filter["published_at"]
            self.filter_sql += 'last_update_date >= \'%s\'' % self.published_at

        self.filter_sql = '1=1' if self.filter_sql == '' else self.filter_sql