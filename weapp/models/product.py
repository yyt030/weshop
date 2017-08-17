#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import datetime

from weapp import db

orderproducts = db.Table('orderproducts',
                         db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
                         db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
                         db.Column('timestamp', db.DateTime, default=datetime.datetime.utcnow))


class Product(db.Model):
    """商品：活动下的商品"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Float(precision=2))
    qty_min = db.Column(db.SmallInteger, default=1)
    qty_max = db.Column(db.SmallInteger, default=100)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    activity = db.relationship('Activity', backref=db.backref('products', lazy='dynamic'))

    orders = db.relationship('Order', secondary=orderproducts, backref=db.backref('products', lazy=True))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        from .activity import Activity
        import forgery_py
        from sqlalchemy.exc import IdentifierError
        seed()
        activity_count = Activity.query.count()
        for i in range(count):
            a = Activity.query.offset(randint(0, activity_count - 1)).first()
            p = Product(name=forgery_py.basic.text(length=5), price=randint(1, 100), activity_id=a.id)

            db.session.add(p)
            try:
                db.session.commit()
            except IdentifierError:
                db.session.rollback()
