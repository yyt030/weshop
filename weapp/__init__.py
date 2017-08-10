#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init app
    db.init_app(app)

    # blueprint
    register_blueprint(app)

    # error handle
    register_error_handle(app)
    return app


def register_error_handle(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return "Yep, I totally not found the page: {}".format(request.url)

    @app.errorhandler(500)
    def inter_error(error):
        abort(500)

    pass


def register_blueprint(app):
    from weapp.controllers import site, api
    app.register_blueprint(site.bp, url_prefix='/')
    app.register_blueprint(api.bp, url_prefix='/interface/')

    pass
