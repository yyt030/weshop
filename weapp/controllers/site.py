#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect

from weapp.models.activity import Activity

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    activities = Activity.query.all()
    return render_template('index.html', activities=activities)


@bp.route('/activities')
def list():
    return redirect('www.baidu.com')


@bp.route('/activity/<int:id>')
def detail(id):
    activity = Activity.query.get_or_404(id)
    return render_template('detail.html', activity=activity)
