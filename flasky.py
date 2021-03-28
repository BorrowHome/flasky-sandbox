# -*- coding: utf-8 -*-

import os

from flask_cors import CORS
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('localhost', 8082), app, handler_class=WebSocketHandler)
    server.serve_forever()
