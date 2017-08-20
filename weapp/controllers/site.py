#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect, url_for

from weapp import db
from weapp.forms.product import ActivityForm, ProductForm, OrderForm
from weapp.models.activity import Activity
from weapp.models.order import Order
from weapp.models.product import Product
from weapp.models.store import Store

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    return redirect(url_for('site.activities'))


@bp.route('/activities')
def activities():
    activities = Activity.query.all()
    return render_template('activities.html', activities=activities)


@bp.route('/activities/<int:id>', methods=['GET', 'POST'])
def activity(id=None):
    form = ActivityForm()
    if form.validate_on_submit():
        pass

    activity = Activity.query.get_or_404(id)
    return render_template('activity.html', activity=activity)


@bp.route('/products/<int:id>', methods=['GET', 'POST'])
def product(id):
    form = OrderForm()
    if form.validate_on_submit():
        p = Product.query.get_or_404(id)
        o = Order(owner_id='1', number=form.number.data, product_id=id)
        db.session.add(o)
        db.session.commit()
        return redirect('/activities/{}'.format(p.activity_id))
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product, form=form)


@bp.route('/orders')
def orders():
    orders = Order.query.all()
    activity_form = ActivityForm()
    product_form = ProductForm()
    print('>>>', Store.get_store_list())
    return render_template('orders.html', orders=orders, activity_form=activity_form, product_form=product_form,
                           stores=Store.get_store_list())


@bp.route('/orders/<int:id>')
def order(id):
    order = Order.query.get_or_404(id)
    return render_template('order.html', order=order)


@bp.route('/stores')
def stores():
    stores = Store.query.all()
    return render_template('stores.html', stores=stores)


@bp.route('/ok')
def ok():
    return render_template('ok.html')
