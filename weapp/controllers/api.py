#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, request
from flask.views import MethodView
from wechatpy import WeChatClient
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import TextReply, EmptyReply
from wechatpy.utils import check_signature

from config import WECHAT_TOKEN, WECHAT_APPID, WECHAT_ENCODING_AES_KEY, WECHAT_WELCOME_MSG, WECHAT_SECRET
from weapp import db
from weapp.models.user import User

bp = Blueprint('api', __name__)


class WechatApi(MethodView):
    def get(self):
        # get var from request args
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')

        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
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
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            # 处理异常情况或忽略
            print('>>> {},{}'.format(request.args, '验证异常'))
            # return '验证异常'
            return 'Shutting down...'
        # 公众号被动接受消息
        if len(request.data) == 0:
            print('>>>', '接收到空字节')
            return ''
        print('>>> [{}]'.format(request.data))
        # 加密方式
        if encrypt_type == 'aes':
            crypto = WeChatCrypto(WECHAT_TOKEN, WECHAT_ENCODING_AES_KEY, WECHAT_APPID)
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
                xml = get_resp_message(decrypted_xml)
                crypto = WeChatCrypto(WECHAT_TOKEN, WECHAT_ENCODING_AES_KEY, WECHAT_APPID)
                encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
                return encrypted_xml
        else:
            # 纯文本方式
            return get_resp_message(request.data)


def get_resp_message(source_msg):
    """构造微信公众号返回消息"""
    request_msg = parse_message(source_msg)
    request_msg_type = request_msg.type
    openid = request.args.get('openid', '')
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
            # 用户关注后，登记用户信息
            try:
                client = WeChatClient(WECHAT_APPID, WECHAT_SECRET)
                user_json = client.user.get(openid)
            except:
                print('>>>', '获取用户信息失败')
            else:
                save_wechat_user(user_json)

            reply = TextReply(content=WECHAT_WELCOME_MSG, message=request_msg)
        elif request_msg_event == 'unsubscribe':
            reply = TextReply(content='多谢关注！', message=request_msg)
        else:
            reply = EmptyReply()
    else:
        reply = EmptyReply()

    # 返回xml报文
    return reply.render()


def save_wechat_user(wechat_user):
    """将微信用户入库"""
    user = User()
    user.openid = wechat_user.get('openid')

    # 该公众号openid 唯一
    isexist = User.query.filter_by(openid=wechat_user.get('openid')).first()
    if isexist:
        return ''

    user.nickname = wechat_user.get('nickname')
    user.subscribe = wechat_user.get('subscribe')
    user.sex = wechat_user.get('sex')
    user.language = wechat_user.get('language')
    user.city = wechat_user.get('city')
    user.province = wechat_user.get('province')
    user.country = wechat_user.get('country')
    user.headimgurl = wechat_user.get('headimgurl')
    user.subscribe_time = wechat_user.get('subscribe_time')
    user.remark = wechat_user.get('remark')
    user.groupid = wechat_user.get('groupid')
    user.tagid_list = ','.join(wechat_user.get('tagid_list'))

    db.session.add(user)
    db.session.commit()


# 添加路由规则
bp.add_url_rule(rule='/', view_func=WechatApi.as_view('api'))
