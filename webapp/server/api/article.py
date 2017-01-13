from flask_restful import Resource, reqparse
from webapp.server.model.model_account import User
from webapp.server.model.model_content import db, ContentArticle


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


class ArticleListApi(Resource):
    def get(self):
        pass

    def post(self):
        pass
