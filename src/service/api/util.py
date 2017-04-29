from src.service.config import SQLConfig
from src.service.model.db_connection import db
from src.service.model.model_content import ContentArticle
from sqlalchemy import func


# @staticmethod
def api_request_parse(result_list=None, page=None):
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
        print('finally')


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
        print('finally')


def sidebar_data():
    recent = ContentArticle.query.order_by(ContentArticle.create_date.desc()).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(tags).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags
