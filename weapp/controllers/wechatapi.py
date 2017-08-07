#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint
from flask.views import MethodView

bp = Blueprint('wechatapi', __name__)


class WechatApi(MethodView):
    def get(self):
        return 'this is get test'

    def post(self):
        return 'this is post test'


bp.add_url_rule(rule='/', view_func=WechatApi.as_view('wechatapi'))
