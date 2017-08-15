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
def init_test_data():
    """导入测试数据"""
    from weapp.models.user import User
    from weapp.models.activity import Activity
    from weapp.models.order import Order
    User.generate_fake()
    Activity.generate_fake()
    Order.generate_fake()


if __name__ == '__main__':
    manager.run()
