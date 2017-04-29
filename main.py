from flask import Flask
from src.www_setting import WwwConfig
from src.service.api.api_source import *
from src.service.model.db_connection import *
from src.webhttp.extension import register_extension


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/
    """
    _app = Flask(__name__, static_folder='./www/static')
    _app.config.from_object(object_name)

    register_api_add_resource(_app)
    register_db_connection(_app)
    register_extension(_app)

    return _app


app = create_app(WwwConfig)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    app.run(host=WwwConfig.Host_URL, port=WwwConfig.Host_Port)
