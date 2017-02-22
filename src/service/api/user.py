from flask_restful import Resource, reqparse
from src.service.config import Conf
from src.service.model.model_account import db, User
from src.service.api.util import api_result


class UserApi(Resource):
    # @staticmethod
    def post(self):
        print(reqparse.request.url)
        print(reqparse.request.path)
        print(reqparse.request.full_path)
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='json')
        parser.add_argument('data', location='json')

        args = parser.parse_args()
        _token = args['token']
        _data = eval(args['data'])
        print(type(_data))

        _userID = _data["topicId"];
        _userName = _data["UserName"]
        _password = _data["Password"]

        _user = User.query.filter_by(id=_userID)
        if _user.count() == 0:
            new_user = User(_userName)
            new_user.password = _password
            db.session.add(new_user)
            db.session.commit()
        elif _user.count() == 1:
            User.query.filter_by(id=_userID).update({
                User.username: _userName,
                User.password: _password
            })
            db.session.commit()
        else:
            print(_user.count())

        if reqparse.request.path == Conf.APIURL_USER_Remove:
            db.session.delete(_user.first())
            db.session.commit()

        _userPage = User.query.order_by(User.id.desc()).paginate(1, 15, False)
        print(type(_userPage.items))
        return api_result(_userPage)
