#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/list')
def list():
    return redirect('www.baidu.com')
