#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, request, current_app
from flask.views import MethodView
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import TextReply, EmptyReply
from wechatpy.utils import check_signature

from weapp import db
from weapp.models.users import User

bp = Blueprint('api', __name__)


class WechatApi(MethodView):
    def get(self):
        # get var from request args
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')

        try:
            check_signature(current_app.config['WECHAT_TOKEN'], signature, timestamp, nonce)
        except InvalidSignatureException:
            # 处理异常情况或忽略
            print('>>> {},{}'.format(request.args, '验证异常'))
            # return '验证异常'
            return 'Shutting down...'
        else:
            print('>>> {},{}'.format(request.args, '验证ok'))
            return echostr

    def post(self):
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        msg_signature = request.args.get('msg_signature', '')
        encrypt_type = request.args.get('encrypt_type', '')
        try:
            check_signature(current_app.config['WECHAT_TOKEN'], signature, timestamp, nonce)
        except InvalidSignatureException:
            # 处理异常情况或忽略
            print('>>> {},{}'.format(request.args, '验证异常'))
            # return '验证异常'
            return 'Shutting down...'
        # 公众号被动接受消息
        if len(request.data) == 0:
            print('>>>', '接收到空字节')
            return ''

        # 加密方式
        if encrypt_type == 'aes':
            crypto = WeChatCrypto(current_app.config[
                                      'WECHAT_TOKEN'], current_app.config['WECHAT_ENCODING_AES_KEY'],
                                  current_app.config[
                                      'WECHAT_APPID'])
            try:
                decrypted_xml = crypto.decrypt_message(
                    request.data,
                    msg_signature,
                    timestamp,
                    nonce
                )
            except (InvalidAppIdException, InvalidSignatureException):
                # to-do: 处理异常或忽略
                print('>>> 加密处理异常')
                return ''
            else:
                xml = self.get_resp_message(decrypted_xml)
                crypto = WeChatCrypto(current_app.config['WECHAT_TOKEN'], current_app.config['WECHAT_ENCODING_AES_KEY'],
                                      current_app.config['WECHAT_APPID'])
                encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
                return encrypted_xml
        else:
            # 纯文本方式
            return self.get_resp_message(request.data)

    @staticmethod
    def get_resp_message(source_msg):
        request_msg = parse_message(source_msg)
        request_msg_type = request_msg.type
        print('>>> request_msg_type[{}],request_msg[{}]'.format(request_msg_type, request_msg))
        # 根据消息类型解析
        if request_msg_type == 'text':
            reply = TextReply(content='{}'.format(request_msg.content), message=request_msg)
        elif request_msg_type == 'image':
            reply = TextReply(content='{}'.format('hello'), message=request_msg)
        elif request_msg_type == 'voice':
            if not request_msg.recognition:
                reply = TextReply(content='没听清楚啊，再说一遍，亲', message=request_msg)
            else:
                reply = TextReply(content='{}'.format(request_msg.recognition), message=request_msg)
        elif request_msg_type == 'event':
            request_msg_event = request_msg.event
            if request_msg_event == 'subscribe':
                user = User(openid=request.args.get('openid'))
                db.session.save(user)

                reply = TextReply(content=current_app.config['WELCOME_MSG'], message=request_msg)
            elif request_msg_event == 'unsubscribe':
                reply = TextReply(content='多谢关注！', message=request_msg)
            else:
                reply = EmptyReply()
        else:
            reply = EmptyReply()

        # 返回xml报文
        return reply.render()


bp.add_url_rule(rule='/', view_func=WechatApi.as_view('api'))
