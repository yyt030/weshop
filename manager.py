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
def create_wechat_menu():
    """create wechat menu"""
    import json

    from wechatpy import WeChatClient
    from config import Config

    client = WeChatClient(Config.WECHAT_APPID, Config.WECHAT_SECRET)
    with open(Config.WECHAT_MENU_FILE) as f:
        client.menu.create(json.load(f))


if __name__ == '__main__':
    manager.run()
