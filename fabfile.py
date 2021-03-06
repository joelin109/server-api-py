from fabric.api import local, run, warn_only, settings, prefix
from fabric.contrib.files import *
import os

'''
$ python3.6 -m pip install fabric3
$ fab install:ops |   fab install  |   fab start:dev


$ fab start
$ fab start:dev
$ fab kill
$ fab gunic
'''


def start(mode='production'):
    kill()

    with settings(warn_only=True):
        result = local('nginx')

        if result.succeeded:
            uwsgi(mode)
            print('start: nginx + uwsgi')


# ps aux | grep uwsgi      :  ps -ef | grep uwsgi
# pkill -f uwsgi -9        :         killall -9 uwsgi
# port is not available after run uwsgi, should visit from nginx
def uwsgi(mode='production'):
    with warn_only():
        local('pkill -f uwsgi -9')

    if mode == 'production':
        local('uwsgi conf/uwsgi.ini')
    else:
        with settings(warn_only=True):
            result = local('uwsgi conf/uwsgi_dev.ini')
            if result.failed:
                print('Run uwsgi failed.')


# ps aux |grep gunicorn      :     ps -ef | grep gunicorn    : pkill -f gunicorn -9
# port is available after run gunicorn
def gunic():
    with settings(warn_only=True):
        result = local('pkill -f gunicorn -9')
        print(result.succeeded)

    # _exec = 'gunicorn -w 3 -b 127.0.0.1:8000 main:app'
    # -b BIND, --bind=BIND,  -c CONFIG, --config=CONFIG
    _exec = 'gunicorn main:app - c conf/gunicorn.conf'

    with prefix('source env/bin/activate'):
        with settings(warn_only=True):
            result = local(_exec)

            if result.failed:
                print('Run gunicorn failed.')


def reload(app='postgres'):
    with settings(warn_only=True):
        local('killall Postgres')

    with settings(warn_only=True):
        result = local('open -a  Postgres')

        if result.failed:
            print('open postgres failed.')


def kill():
    # '/usr/local/etc/nginx/nginx.conf'
    with settings(warn_only=True):
        result_nginx = local('pkill -f nginx -9')

    with settings(warn_only=True):
        result_uwsgi = local('pkill -f uwsgi -9')

    with settings(warn_only=True):
        result_guni = local('pkill -f gunicorn -9')

    if result_nginx.failed:
        print('non-uwsgi process')
    else:
        print('nginx process killed done.')

    if result_uwsgi.failed:
        print('non-uwsgi process')
    else:
        print('uwsgi process killed done.')

    if result_guni.succeeded:
        print('gunicorn process killed done.')
    else:
        print('non gunicorn process')


'''

# install ops package for python3.6
# install necessary package for the project

$ fab install:ops
$ fab install

'''


# install python package
def install(pip='default'):
    if pip == 'ops':
        _pip_install_ops()

    else:
        _pip_install()


def _pip_install_ops():
    result = local('python3.6 -m pip install -r requirements_ops.txt')
    if result.succeeded:
        print('python3.6 -m pip install succeeded')
    else:
        print('python3.6 -m pip install failed')


def _pip_install():
    _virtualenv = True
    if os.path.isdir('env/bin/') is not True:
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

            if result.succeeded:
                local('pip install -r requirements_next.txt')


'''

# Connect to ec2, then update... 

$ fab ec2

$ fab update
$ fab update:1


'''


def ec2():
    _connect_ec2()


def _connect_ec2():
    _ssh_ec2_local_path = '/Volumes/Mac-TBD/Server/aws-ec2'
    _ssh_ec2_pem_file = 'sing-ub-py.pem'
    _ssh_ec2 = 'ec2-52-221-45-133.ap-southeast-1.compute.amazonaws.com'

    with prefix('cd ' + _ssh_ec2_local_path):
        _pem_result = local('chmod 400 ' + _ssh_ec2_pem_file)
        _ssh_connect_exec = 'ssh -i "%s" ubuntu@%s' % (_ssh_ec2_pem_file, _ssh_ec2)

        if _pem_result.failed:
            print("pem file failed.")
        if _pem_result.succeeded:
            _ssh_connect_result = local(_ssh_connect_exec)

            if _ssh_connect_result.failed:
                print("ssh connect ec2 failed.")
            else:
                print('dfdsfdsf')
                with prefix('cd /home/ubuntu/api36/server-api-py'):
                    print('dfdsfdsf')
                    _ec2_result = run('python -V ')
                    print(_ec2_result)


# fab update  | fab update:1
def update(will_login=False):
    with settings(warn_only=True):
        result = local('ansible-playbook ansible/pb_ec2.yml')

        if result.succeeded and will_login:
            _connect_ec2()