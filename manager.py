#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import os

from flask_script import Manager

from weapp import create_app

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
