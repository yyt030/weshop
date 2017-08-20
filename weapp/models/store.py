#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from datetime import datetime

from weapp import db


class Store(db.Model):
    """仓库：记录商品的优惠信息"""
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price_source = db.Column(db.Float(.2), nullable=True)
    price_advice = db.Column(db.Float(.2), nullable=True)
    remark = db.Column(db.String(64))

    create_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.id)

    @property
    def to_json(self):
        columns = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in columns}

    @staticmethod
    def get_store_list():
        stores = Store.query.all()
        return [{'title': '{}-团购价:{}'.format(s.name, s.price_advice), 'value': s.id} for s in
                stores]

    @staticmethod
    def generate_fake():
        pass
        s1 = Store(name='新西兰爱妃', price_source='238', price_advice='195', remark='新西兰爱妃5kg礼盒装，妃你莫属的浓甜滋味，原价238，团购价195')
        s2 = Store(name='美国夏橙', price_source='238', price_advice='195', remark='新西兰爱妃5kg礼盒装，妃你莫属的浓甜滋味，原价238，团购价195')
        s3 = Store(name='美国恐龙蛋', price_source='238', price_advice='195', remark='新西兰爱妃5kg礼盒装，妃你莫属的浓甜滋味，原价238，团购价195')
        s4 = Store(name='美国大西梅', price_source='238', price_advice='195', remark='新西兰爱妃5kg礼盒装，妃你莫属的浓甜滋味，原价238，团购价195')
        s5 = Store(name='美国夏橙', price_source='238', price_advice='195', remark='新西兰爱妃5kg礼盒装，妃你莫属的浓甜滋味，原价238，团购价195')
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.add(s4)
        db.session.add(s5)
        db.session.commit()
