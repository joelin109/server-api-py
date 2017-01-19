from flask import Flask
from webapp.conf.config import BasicConfig
from webapp.server.api.api_source import *
from webapp.server.model.db_connection import *

from webapp.uicontroller.blueprint import register_blueprint
from webapp.uicontroller.extension_admin import register_admin
from webapp.uicontroller.extension_login import register_login
import asyncio


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/
    """
    _app = Flask(__name__)
    _app.config.from_object(object_name)

    register_api_add_resource(_app)
    register_db_connection(_app)
    register_blueprint(_app)
    register_admin(_app)
    register_login(_app)

    return _app


app = create_app(BasicConfig)
if __name__ == '__main__':
    app.run(host=BasicConfig.Host_URL, port=BasicConfig.Host_Port)

"""
async def async_foo():
    print("async_foo started")
    await asyncio.sleep(4)
    print('Do some actions 1')
    await asyncio.sleep(2)
    print('Do some actions 2')
    return "async_foo return"


async def main():
    # asyncio.ensure_future(async_foo())  # fire and forget async_foo()

    # btw, you can also create tasks inside non-async funcs

    print('Do some actions 1')
    await asyncio.sleep(1)
    print('Do some actions 2')
    await asyncio.sleep(1)
    print('Do some actions 3')


if __name__ == '__main__':
    print('get_event_loop')
    loop = asyncio.get_event_loop()
    print('run_until_complete')
    #ss = loop.run_until_complete(async_foo())
    ss = async_foo()
    print(ss)
    print("fdgfdgfdgd")
 """
