from fabric.api import local, run, warn_only, settings, prefix
from fabric.contrib.files import *
import os


# fab kill/start
def start():
    kill()
    with settings(warn_only=True):
        result = local('nginx')

        if result.succeeded:
            uwsgi()
            print('start: nginx + uwsgi')


# ps aux | grep uwsgi      :  ps -ef | grep uwsgi
# pkill -f uwsgi -9        :         killall -9 uwsgi
# port is not available after run uwsgi, should visit from nginx
def uwsgi():
    with warn_only():
        local('pkill -f uwsgi -9')

    local('uwsgi conf/uwsgi.ini')


# ps aux |grep gunicorn      :     ps -ef | grep gunicorn    : pkill -f gunicorn -9
# port is available after run gunicorn
def gunic():
    with settings(warn_only=True):
        result = local('pkill -f gunicorn -9')
        print(result.succeeded)

    # _exec = 'gunicorn -w 3 -b 127.0.0.1:8000 main:app'
    # -b BIND, --bind=BIND,  -c CONFIG, --config=CONFIG
    _exec = 'gunicorn main:app - c conf/gunicorn.conf'
    with settings(warn_only=True):
        result = local(_exec)

        if result.failed:
            with prefix('source env/bin/activate'):
                local(_exec)


def kill():
    # '/usr/local/etc/nginx/nginx.conf'
    with settings(warn_only=True):
        result = local('pkill -f nginx -9')

    with settings(warn_only=True):
        result = local('pkill -f uwsgi -9')
        if result.failed:
            print('non uwsgi process')

    with settings(warn_only=True):
        result = local('pkill -f gunicorn -9')
        if result.succeeded:
            print('killed.')
        else:
            print('non gunicorn process')

    # if exists('env/'):


def install():
    _virtualenv = True
    if os.path.isdir('env/') is not True:
        with settings(warn_only=True):
            result = local('virtualenv env')
            _virtualenv = result.succeeded
            print('virtualenv env')

    else:
        print('Already have env.')

    if _virtualenv:
        # deactivate
        with prefix('source env/bin/activate'):
            result = local('pip install -r requirements.txt')

            # psycopg2==2.7.1
            # Scrapy==1.4.0
            if result.succeeded:
                local('pip install psycopg2')
                local('pip install scrapy')
