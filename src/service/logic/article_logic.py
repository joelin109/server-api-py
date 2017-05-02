from src.service.model.model_content import db, ContentArticle, ContentDictionary
from src.service.logic.util_logic import UtilLogic
from datetime import datetime
from src.service.crawler.article_body import crawl_article_body
from src.service.util.logger import *


class ArticleLogic(UtilLogic):
    def new(self, new_article):
        self._verify_except_case()
        try:
            db.session.add(new_article)
            db.session.commit()
        except:
            db.session.rollback()
            raise

        return True

    def update_aticle(self, article):
        self._verify_except_case()

        ContentDictionary.query.filter_by(id=article.id).update({
            ContentArticle.format_type: article.format_type,
            ContentArticle.body_text: article.body_text,
            ContentArticle.body_parse_level: article.body_parse_level,
            ContentArticle.publish_status: article.publish_status,
            ContentArticle.is_recommend: article.is_recommend,
            ContentArticle.last_update_date: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        db.session.commit()
        return True

    def update_aticle_body(self, article):
        self._verify_except_case()

        ContentDictionary.query.filter_by(id=article.id).update({
            ContentArticle.format_type: article.format_type,
            ContentArticle.body_text: article.body_text,
            ContentArticle.body_parse_level: article.body_parse_level,
            ContentArticle.publish_status: article.publish_status,
            ContentArticle.is_recommend: article.is_recommend,
            ContentArticle.last_update_date: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        db.session.commit()
        return True

    def get_list(self, list_filter=None):
        try:
            if list_filter is None:
                list_filter = ArticleListFilter()

            print(str(list_filter.page_num) + '   |  ' + str(list_filter.page_size))
            _listResult = ContentArticle.query.filter(list_filter.filter_sql) \
                .order_by(ContentArticle.last_update_date.desc()) \
                .paginate(list_filter.page_num, list_filter.page_size, False)

        except Exception as ex:
            raise RuntimeError(ex)

        print(_listResult.items[0].title)
        return self.result_page(_listResult)

    def get_top_list(self, filter_tag_id, filter_date):
        self._verify_except_case()
        try:
            _filter_sql = 'tag_id = \'%s\' AND last_update_date >= \'%s\'' % (filter_tag_id, filter_date)
            _listResult = ContentArticle.query.filter(_filter_sql).paginate(1, 100, False)

        except Exception as ex:
            raise RuntimeError(ex)

        _result_row = [m.parse_top() for m in _listResult.items]
        return _result_row

    def get_detail(self, article_id, original_url=None):
        self._verify_except_case()

        _result = dict()
        _result["id"] = article_id
        _result["original_url"] = original_url
        _result["body_text"] = crawl_article_body(original_url)

        # _word = ContentArticle.query.filter_by(id=article_id).first()
        return _result


class ArticleListFilter:
    page_num = 1
    page_size = 100
    publish_status = 1
    is_recommend = 0
    published_at = ""
    publish_status = -1
    filter_sql = "1=1"

    def parse(self, data_filter=None):
        self.page_num = 1 if 'page_num' not in data_filter else data_filter['page_num']

        if 'page_size' in data_filter:
            self.page_size = data_filter['page_size']
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
