# -*- coding:UTF8 -*-
from flask import Flask, request, make_response
from xml.etree import cElementTree
import hashlib
from datetime import datetime
from wx_lib.config import GetConfig
from wx_lib.base import WXBase, StorageUser
import sys
import logging
import re

# 　配置微信回调接口秘钥
TOKEN = "1780ea515b9dc9bf"


def sha1(data):
    m = hashlib.sha1()
    m.update(data.encode('utf-8'))
    return m.hexdigest()


app = Flask(__name__)

CONFIG = GetConfig(sys.path[0])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        signature = request.args.get('signature')
        echo_str = request.args.get('echostr')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        if not echo_str or not signature or not timestamp or not nonce:
            return make_response("参数错误...")
        if sha1(''.join(sorted([TOKEN, timestamp, nonce]))) == signature.strip():
            return echo_str.strip()
        else:
            return make_response("签名校验失败...")
    else:
        msg = """<xml>
        <ToUserName><![CDATA[{openid}]]></ToUserName>
        <FromUserName><![CDATA[{from_username}]]></FromUserName>
        <CreateTime>{time}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{content}]]></Content>
        </xml>"""
        content = "不支持该事件"
        xml_data = cElementTree.fromstring(request.stream.read())
        msg_type = xml_data.find("MsgType").text
        open_id = xml_data.find("FromUserName").text
        from_username = xml_data.find("ToUserName").text
        if msg_type.strip() == "event" and xml_data.find("Event").text == "subscribe":
            content = """欢迎关注运维报警微信,请直接回复邮箱地址绑定"""
        elif msg_type.strip() == "event" and xml_data.find("Event").text == "unsubscribe":
            storage = StorageUser(sys.path[0])
            target_open_id = storage.remove(open_id.strip())
            if target_open_id is not None:
                logging.info("{nick_name}解除{mail}邮箱绑定成功...".format(nick_name=target_open_id["nick_name"],
                                                                   mail=target_open_id["email"]))
            return make_response("")
        elif msg_type.strip() == "text":
            mail = xml_data.find("Content").text
            if not re.match(r".*@[A-Za-z_]+.[a-z]+", mail):
                content = """您的邮箱{mail}邮箱格式错误,请输入正确的邮箱格式...""".format(mail=mail)
                return make_response(msg.format(
                    **{'openid': open_id, 'from_username': from_username, 'time': str(datetime.now().timestamp()),
                       'content': content}))
            storage = StorageUser(sys.path[0])
            target_open_id = list(filter(lambda x: x["open_id"].strip() == open_id.strip(), storage.read()))
            if target_open_id:
                nick_name = target_open_id[0]["nick_name"]
                mail = target_open_id[0]["email"]
                content = """{nick_name},您的邮箱{mail}已经绑定,请不要重复绑定...""".format(nick_name=nick_name, mail=mail)
                return make_response(msg.format(
                    **{'openid': open_id, 'from_username': from_username, 'time': str(datetime.now().timestamp()),
                       'content': content}))
            token = CONFIG.get_config()
            if token is None:
                content = """您的邮箱{mail}绑定失败...""".format(mail=mail)
                return make_response(msg.format(
                    **{'openid': open_id, 'from_username': from_username, 'time': str(datetime.now().timestamp()),
                       'content': content}))
            wx_obj = WXBase(token["app_id"], token["secret"], sys.path[0])
            wx_obj.get_token()
            nick_name = wx_obj.nick_name_get(open_id)
            if nick_name is None:
                content = """邮箱{mail}绑定失败, 请联系管理员...""".format(mail=mail)
                logging.warning(content)
            else:
                storage = StorageUser(sys.path[0])
                storage.write(open_id.strip(), nick_name.strip(), mail.strip())
                content = """{nick_name},您的邮箱{mail}绑定成功,现在开始您可以收到报警信息...""".format(nick_name=nick_name, mail=mail)
                logging.info(content)
        return make_response(msg.format(
            **{'openid': open_id, 'from_username': from_username, 'time': str(datetime.now().timestamp()),
               'content': content}))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=80, debug=False)
