import os

_exec = 'uwsgi --ini uwsgi.ini'
os.system(_exec)

# uwsgi --ini uwsgi.ini
# pkill -f uwsgi -9
# killall -9 uwsgi