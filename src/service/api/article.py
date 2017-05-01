from flask_restful import Resource, reqparse
from src.service.api.util import api_response_format, api_request_parse
from src.service.model.model_content import db, ContentArticle
from src.service.logic.article_logic import ArticleLogic, ArticleListFilter


class ArticleApi(Resource):
    def get(self, post_id=None):
        if post_id:
            db.session.commit()
            users = User.query.filter_by(id=post_id).first()
            return {"Hello": users.username}

        return {"Hello": "Joe"}

    def post(self, post_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='json')
        parser.add_argument('data', location='json')
        args = parser.parse_args()
        _userToken = args['token']
        _userData = args['data']
        return {"Token": _userToken, "Data": _userData}


class ArticleStatusApi(Resource):
    def get(self):
        pass

    def post(self):
        _request_data = api_request_parse()

        print(_request_data)
        return _request_data


class ArticleListApi(Resource):
    def get(self):
        pass

    def post(self):
        _request_data = api_request_parse()

        _list_filter = _get_request_data_filter(_request_data)
        _logic = ArticleLogic()
        _result_list, _page = _logic.get_list(_list_filter)
        return api_response_format(_result_list, _page)


def _get_request_data_filter(request_data):
    if 'filter' in request_data:
        _request_data_filter = request_data["filter"]

        _list_filter = ArticleListFilter()
        _list_filter.parse(_request_data_filter)
        return _list_filter

    else:
        return None
