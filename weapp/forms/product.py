#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField


class ProductForm(FlaskForm):
    number = IntegerField('预定单数', render_kw={'placeholder': "输入预定单数"})
    submit = SubmitField('预定')
