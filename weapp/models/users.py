#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from  datetime import datetime

from weapp import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(28), unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String(64), index=True)
    subscribe = db.Column(db.SmallInteger)
    sex = db.Column(db.SmallInteger)
    language = db.Column(db.String(10))
    city = db.Column(db.String(64))
    province = db.Column(db.String(64))
    country = db.Column(db.String(64))
    headimgurl = db.Column(db.Text)
    subscribe_time = db.Column(db.BigInteger)
    remark = db.Column(db.String(64))
    groupid = db.Column(db.SmallInteger)
    tagid_list = db.Column(db.Text)

    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<User {}-{}: {}>'.format(id, self.openid, self.username)
