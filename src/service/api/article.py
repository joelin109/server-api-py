from flask_restful import Resource, reqparse
from src.service.api.util import api_response_format, api_response_detail_format, api_request_parse
from src.service.model.model_content import ContentArticle
from src.service.logic.article_logic import ArticleLogic, ArticleListFilter


class ArticleApi(Resource):
    def get(self, post_id=None):
        _name = "Joe" if post_id is None else post_id
        return {"Hello": _name}

    def post(self, post_id=None):
        print('ArticleApiArticleApiArticleApiArticleApiArticleApiArticleApiArticleApiArticleApi')
        _request_data = api_request_parse()
        print(_request_data)
        _article = _get_request_data(_request_data)
        _logic = ArticleLogic()
        _result = _logic.update_aticle_body(_article)

        return api_response_detail_format(_result)


class ArticleStatusApi(Resource):
    def post(self):
        _request_data = api_request_parse()

        _article = ContentArticle('')
        _article.id = _request_data["id"]
        _article.is_recommend = _request_data["is_recommend"]
        _article.publish_status = _request_data["publish_status"]

        _logic = ArticleLogic()
        _request_data['result'] = _logic.update_aticle_status(_article)

        return api_response_detail_format(_request_data)


class ArticleListApi(Resource):
    def get(self):
        pass

    def post(self):
        _request_data = api_request_parse()

        _list_filter = _get_request_data_filter(_request_data)
        _logic = ArticleLogic()
        _result_list, _page = _logic.get_list(_list_filter)
        return api_response_format(_result_list, _page)


class ArticleDetailApi(Resource):
    def post(self, post_id=None):
        print(
            'ArticleDetailApiArticleDetailApiArticleDetailApiArticleDetailApiArticleDetailApiArticleDetailApiArticleDetailApi')
        _request_data = api_request_parse()
        _article_id = _request_data["id"]
        print(_request_data)
        _logic = ArticleLogic()
        _result_detail = _logic.get_detail(_article_id)

        return api_response_detail_format(_result_detail)


def _get_request_data(request_data):
    # print(request_data)
    _article = ContentArticle('')
    _article.id = request_data["id"]
    _article.title = request_data["title"]
    _article.cover_src = request_data["cover_src"]
    # request_data["body_match_level"]
    _article.body_match_level = 3
    _article.body_text = request_data["body_text"]

    print(_article.id + '     |      ' + _article.title)
    return _article


def _get_request_data_filter(request_data):
    if 'filter' in request_data:
        _request_data_filter = request_data["filter"]

        _list_filter = ArticleListFilter()
        _list_filter.parse(_request_data_filter)
        return _list_filter

    else:
        return None
