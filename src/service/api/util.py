from src.service.config import SQLConfig
from flask_restful import reqparse


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
def api_response_format(result_list=None, page=None):
    try:

        _results = {
            "page": page,
            "rows": result_list
        }
        _response = {
            "code": 1,
            "desc": "success",
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
