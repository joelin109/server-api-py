from flask_restful import Resource, reqparse
from src.service.config import Conf
from src.service.model.model_account import User
from src.service.api.util import api_response_format
from src.service.logic.user_logic import UserLogic


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

        _logic = UserLogic()
        _user = _logic.get_detail(_userID)

        if _user is None:
            new_user = User(_userName)
            new_user.password = _password
            _logic.new(new_user)
        else:
            _logic.update(_user)

        if reqparse.request.path == Conf.APIURL_USER_Remove:
            _logic.delete(_user)

        _userPage = _logic.get_list()
        return api_response_format(_userPage)
