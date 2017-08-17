#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from weapp import db


class Store(db.Model):
    """仓库：记录商品的优惠信息"""
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    remark = db.Column(db.String(64))

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.id)

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py
        from sqlalchemy.exc import IntegrityError

        seed()
        for i in range(count):
            s = Store(name=forgery_py.name.full_name(), remark=forgery_py.basic.text(length=30))
            db.session.add(s)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()