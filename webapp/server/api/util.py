from webapp.server.config import SQLConfig
from webapp.server.model.db_connection import db
from webapp.server.model.model_content import ContentArticle
from sqlalchemy import func


# @staticmethod
def api_result(result_list=None, page=None):
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
