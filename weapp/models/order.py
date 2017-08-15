#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from weapp import db


class OrderStatus(object):
    INIT = 0
    DONE = 1


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', backref='orders', lazy='dynamic')
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    activity = db.relationship('Activity', backref='orders', lazy='dynamic')
    number = db.Column(db.Integer, default=1, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.id)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import randint, seed
        from .user import User
        from .activity import Activity

        user_count = User.query.count()
        activity_count = Activity.query.count()

        seed()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            a = Activity.query.offset(randint(0, activity_count - 1)).first()
            o = Order(owner_id=u.id, activity_id=a.id, number=randint(1, 100))

            db.session.add(o)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
