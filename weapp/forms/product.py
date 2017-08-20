#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, DateField, FloatField


class ActivityForm(FlaskForm):
    title = StringField('活动标题', render_kw={'placeholder': "输入活动标题"})
    remark = StringField('活动说明', render_kw={'placeholder': "输入关于该活动的描述"})
    expire_date = DateField('活动截止时间')
    submit = SubmitField('创建')


class ProductForm(FlaskForm):
    name = StringField('商品标题', render_kw={'placeholder': "输入商品标题"})
    price = FloatField('商品价格', render_kw={'placeholder': "输入商品价格"})

    submit = SubmitField('发布')


class OrderForm(FlaskForm):
    number = IntegerField('预定单数', render_kw={'placeholder': "输入预定单数"})
    submit = SubmitField('预定')
