#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from datetime import datetime

from weapp import db


class OrderStatus(object):
    INIT = 0
    DONE = 1


class OrderProduct(db.Model):
    __tablename__ = 'OrderProducts'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', backref=db.backref('orders', lazy='dynamic'))
    number = db.Column(db.Integer, default=1, nullable=False)
    status = db.Column(db.SmallInteger, default=1, nullable=False)

    products = db.relationship('Product', secondary='OrderProduct',
                               foreign_keys=[OrderProduct.order_id],
                               backref=db.backref('orders', lazy='dynamic')
                               )

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.id)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import randint, seed
        from .user import User
        from .product import Product

        user_count = User.query.count()
        product_count = Product.query.count()

        seed()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Product.query.offset(randint(0, product_count - 1)).first()
            o = Order(owner_id=u.id, number=randint(1, 100), status=1)

            o.products.append(p)
            db.session.add(o)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
