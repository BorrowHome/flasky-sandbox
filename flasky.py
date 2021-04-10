# -*- coding: utf-8 -*-
import os
import sys

from app import create_app

print('init base time ')
basedir, filename = os.path.split(os.path.abspath(sys.argv[0]))
app = create_app(basedir=basedir)
print('main to  ', basedir)
app.__setattr__('static_folder', basedir + '\\app\\static')
if __name__ == '__main__':
    # server = pywsgi.WSGIServer(('localhost', 8082), app)
    # server.serve_forever()
    app.run('localhost', '8082', debug=True, threaded=True)
