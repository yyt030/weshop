#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from weapp import create_app, db

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_wechat():
    """初始化微信信息，菜单，模板"""
    pass


if __name__ == '__main__':
    manager.run()
