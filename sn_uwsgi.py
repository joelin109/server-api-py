import os

_exec = 'uwsgi uwsgi.ini'
os.system('pkill -f uwsgi -9')
os.system(_exec)

# uwsgi uwsgi.ini

# ps aux | grep uwsgi      :  ps -ef | grep uwsgi
# pkill -f uwsgi -9        :         killall -9 uwsgi
