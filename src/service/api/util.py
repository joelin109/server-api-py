from flask_restful import Resource, reqparse
from datetime import datetime
from enum import Enum
from src.service.config import SQLConfig


class Http(Enum):
    Request = 0
    Response = 1
    Response_detail = 2


class Api(Resource):
    token: str = ''
    permitted: bool = True

    def __init__(self):
        self.http_start_time = datetime.now()

    def request_data(self, parser=None):
        self.token = ''
        self.permitted = True
        return api_request_parse(parser)

    def response(self, result_list, page):
        _performance = self._calculate_performance()
        return api_response_format(result_list, page, _performance)

    def response_detail(self, result_detail):
        return api_response_detail_format(result_detail)

    def without_permit(self):
        self.token = ''
        return api_response_format_err('error token')

    def _calculate_performance(self):
        _request_end_time = datetime.now()
        _request_gap = _request_end_time - self.http_start_time

        _performance = {
            "http_start": self.http_start_time.strftime('%m-%d %H:%M:%S_%f'),
            "http_end": _request_end_time.strftime('%m-%d %H:%M:%S_%f'),
            "http_use": '%s s' % (_request_gap.seconds + (_request_gap.microseconds // 1000)/1000)
        }
        return _performance


# @staticmethod
def api_request_parse(parser=None):
    if parser is None:
        parser = reqparse.RequestParser()

    parser.add_argument('token', type=str, location='json')
    parser.add_argument('data', location='json')
    _args = parser.parse_args()
    _token = _args['token']
    _data = eval(_args['data'])
    return _data


# @staticmethod
def api_response_format(result_list=None, page=None, performance=None):
    try:

        _results = {
            "page": page,
            "rows": result_list
        }
        _response = {
            "code": 1,
            "desc": "success",
            "perf": performance,
            "resource": SQLConfig.SQLALCHEMY_DATABASE_URI.split(":")[0],
            "result": _results
        }
        return _response

    except IOError as error:
        return {"error": "I/O error: {0}".format(error)}
    except:
        return {"error": "........"}
        raise
    finally:
        print('api_response_format - finally - Done')


def api_response_format_err(reason):
    try:
        _response = {
            "code": 0,
            "desc": "failure",
            "resource": SQLConfig.SQLALCHEMY_DATABASE_URI.split(":")[0],
            "result": [],
            "error": reason
        }
        return _response

    except:
        return {"error": "........"}
        raise
    finally:
        print('api_response_format - finally - Done')


def api_response_detail_format(result=None):
    try:
        _response = {
            "code": 1,
            "desc": "success",
            "resource": SQLConfig.SQLALCHEMY_DATABASE_URI.split(":")[0],
            "result": result
        }
        return _response

    except IOError as error:
        return {"error": "I/O error: {0}".format(error)}
    except:
        return {"error": "........"}
        raise
    finally:
        print('api_response_detail_format - finally - Done')
