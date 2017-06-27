from src.service.api.util import Api
from src.service.model.model_content import ContentArticle
from src.service.logic.article_logic import ArticleLogic, ArticleListFilter


# Create or modify article
class ArticleApi(Api):
    def get(self, post_id=None):
        _name = "Joe" if post_id is None else post_id
        return {"Hello": _name}

    def post(self, post_id=None):
        _request_data = self.request_data()
        if self.permitted is False:
            return self.without_permit()

        print(_request_data)
        _article = _get_request_data(_request_data)
        _logic = ArticleLogic()
        _result = _logic.update_article_body(_article)

        return self.response_detail(_result)


class ArticleStatusApi(Api):
    def post(self):
        _request_data = self.request_data()
        if self.permitted is False:
            return self.without_permit()

        _article = ContentArticle('')
        _article.id = _request_data["id"]
        _is_recommend = _request_data["is_recommend"]
        _article.is_recommend = True if _is_recommend == 1 or _is_recommend else False
        _article.publish_status = _request_data["publish_status"]

        _logic = ArticleLogic()
        _request_data['result'] = _logic.update_article_status(_article)

        return self.response_detail(_request_data)


class ArticleListApi(Api):
    def get(self):
        pass

    def post(self):
        _request_data = self.request_data()
        if self.permitted is False:
            return self.without_permit()

        _list_filter = _get_request_data_filter(_request_data)
        _logic = ArticleLogic()
        _result_list, _page = _logic.get_list(_list_filter)

        return self.response(_result_list, _page)


class ArticleDetailApi(Api):
    def post(self, post_id=None):
        _request_data = self.request_data()

        _article_id = _request_data["id"]
        print(_request_data)
        _logic = ArticleLogic()
        _result_detail = _logic.get_detail(_article_id)

        return self.response_detail(_result_detail)


def _get_request_data(request_data):
    # print(request_data)
    _article = ContentArticle('')
    _article.id = request_data["id"]
    _article.title = request_data["title"]
    _is_recommend = request_data["is_recommend"]
    _article.is_recommend = True if _is_recommend == 1 or _is_recommend else False

    _article.publish_status = request_data["publish_status"]
    _article.cover_src = request_data["cover_src"]
    # request_data["body_match_level"]
    _article.body_text = request_data["body_text"]
    _article.body_match_level = -1 if len(_article.body_text) < 10 else 3

    print(_article.id + ': ' + _article.title + '  |  '
          + str(_article.body_match_level) + ' | ' + str(_article.publish_status))
    return _article


def _get_request_data_filter(request_data):
    if 'filter' in request_data:
        _request_data_filter = request_data["filter"]

        _list_filter = ArticleListFilter()
        _list_filter.parse(_request_data_filter)
        return _list_filter

    else:
        return None
