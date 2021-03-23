# -*- coding: utf-8 -*-

import os

from flask_cors import CORS

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(host="localhost", port=8082, debug=True)
