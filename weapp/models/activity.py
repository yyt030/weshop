#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from datetime import datetime

from weapp import db
from weapp.models.user import User


class Activity(db.Model):
    """由组织人发起的活动"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    remark = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', backref=db.backref('activities', lazy='dynamic'))
    headimgurl = db.Column(db.String(128))
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.id)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint, choice
        from sqlalchemy.exc import IntegrityError
        import os
        from config import basedir

        seed()
        user_count = User.query.count()
        with open(os.path.join(basedir, 'tests/words')) as f:
            words_list = f.read().split()
            for i in range(count):
                u = User.query.offset(randint(0, user_count - 1)).first()
                o = Activity(title=choice(words_list), remark=choice(words_list), owner_id=u.id)
                db.session.add(o)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
