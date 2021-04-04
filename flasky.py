# -*- coding: utf-8 -*-
import os

from app import create_app

print('init base time ')
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
basedir = os.path.abspath(os.path.dirname(__file__))
print('main to  ', basedir)
app.__setattr__('static_folder', basedir + '\\app\\static')
if __name__ == '__main__':
    # server = pywsgi.WSGIServer(('localhost', 8082), app)
    # server.serve_forever()
    app.run('localhost', '8082', debug=True, threaded=True)
