#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Flask

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # blueprint
    register_blueprint(app)

    # error handle
    # register_error_handle(app)
    return app


def register_error_handle(app):
    @app.exception(404)
    def ignore_404(request, exception):
        # return text("Yep, I totally found the page: {}".format(request.url))
        pass

    @app.exception(500)
    def ignore_500(request, exception):
        # return 505
        pass

    pass


def register_blueprint(app):
    from weapp.controllers import site, wechatapi
    app.register_blueprint(site.bp, url_prefix='/')
    app.register_blueprint(wechatapi.bp, url_prefix='/interface')

    pass
