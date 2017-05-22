import os

_exec = 'uwsgi uwsgi.ini'
os.system(_exec)

# uwsgi uwsgi.ini
# ps -ef | grep uwsgi
# pkill -f uwsgi -9        :         killall -9 uwsgi
