#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from datetime import datetime

from weapp import db
from weapp.models.user import User


class Activity(db.Model):
    """发起活动"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    remark = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', backref=db.backref('activities', lazy='dynamic'))
    headimgurl = db.Column(db.String(128))
    create_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.id)

    @staticmethod
    def generate_fake(count=100):
        import forgery_py
        from random import seed, randint
        from sqlalchemy.exc import IntegrityError

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            o = Activity(title=forgery_py.basic.text(length=32), remark=forgery_py.name.title(), owner_id=u.id)
            db.session.add(o)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
