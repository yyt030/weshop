#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import json

from wechatpy import WeChatClient

from config import WECHAT_APPID, WECHAT_SECRET, WECHAT_MENU_FILE


def create_wechat_menu():
    """create wechat menu"""

    print('>>>>', WECHAT_APPID, WECHAT_SECRET)
    client = WeChatClient(WECHAT_APPID, WECHAT_SECRET)

    with open(WECHAT_MENU_FILE) as f:
        client.menu.create(json.load(f))


def init_template_message():
    """发送模板文本消息"""

    client = WeChatClient(WECHAT_APPID, WECHAT_SECRET)
    # res = client.template.set_industry(1, 4)
    # print('>>>', res)
    res = client.template.get_industry()
    print('>>>', res)


def get_all_template():
    """获取模板列表"""

    client = WeChatClient(WECHAT_APPID, WECHAT_SECRET)
    res = client.template.get_all_private_template()
    print('>>>', res)


def add_template():
    """添加模板"""
    print('>>>', WECHAT_APPID, WECHAT_SECRET)
    client = WeChatClient(WECHAT_APPID, WECHAT_SECRET)
    res = client.template.add('TM00015')
    print('>>>', res)


def send_template_message():
    import os
    client = WeChatClient(WECHAT_APPID, WECHAT_SECRET)
    data = {
        "first": {
            "value": "恭喜你购买成功！",
            "color": "#173177"
        },
        "Remark": {
            "value": "感谢您的使用，请继续关注我们新的优惠活动！",
        },
        "orderProductName": {
            "value": "商品１",
            "color": "#173177"
        },
        "orderMoneySum": {
            "value": "999.9元",
            "color": "#173177"
        }
    }
    client.message.send_template(user_id=os.environ.get('WECHAT_OPENID'),
                                 template_id=os.environ.get('WECHAT_TEMPID'),
                                 data=data)


if __name__ == '__main__':
    pass
    # add_template()
    # send_template_message()
    # get_all_template()
    # create_wechat_menu()
