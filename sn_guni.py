import os

_exec = 'gunicorn -w 3 -b 127.0.0.1:8000 main:app'
os.system(_exec)

# exec gunicorn -w 3 -b 0.0.0.0:8080 main:app
# ps aux |grep gunicorn      :     ps -ef | grep gunicorn
# pkill -f gunicorn -9
