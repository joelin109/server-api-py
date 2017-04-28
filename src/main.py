from flask import Flask
from src.www_setting import WwwConfig
from src.service.api.api_source import *
from src.service.model.db_connection import *
from src.webhttp.extension import register_extension

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
