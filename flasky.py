# -*- coding: utf-8 -*-

import os

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# 单元测试
@app.cli.command()
def test():
    """ run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
