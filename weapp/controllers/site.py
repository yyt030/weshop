#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint,request

bp = Blueprint('site', __name__)


@bp.route('/',methods=['GET','POST'])
def index():
    print('>>>>', request.data)
    return 'hello world'
