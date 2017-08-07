#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    return 'hello world'
