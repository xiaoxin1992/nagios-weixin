# -*- coding:UTF8 -*-
import requests
from datetime import datetime
import json
import logging
import os


class WXBase:
    def __init__(self, app_id, app_secret, config):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://api.weixin.qq.com"
        self.config_token = os.path.join(config, "conf", "token.json")
        self.token = None

    @staticmethod
    def request(url, method="get", timeout=20, data=None):
        """
        执行http请求, 根据不同method执行不同操作
        :param url:
        :param method:
        :param timeout:
        :param data:
        :return:
        """
        try:
            return getattr(requests, method)(url, timeout=timeout, data=data)
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, AttributeError) as e:
            logging.error("{error}...".format(error=str(e)))
        return None

    def get_token(self):
        """
        获取Token
        如果成功返回token 如果失败返回None
        :return: token
        """
        try:
            with open(self.config_token, "r") as f:
                token_data = json.load(f)
            if token_data["expires_time"] > datetime.now().timestamp():
                self.token = token_data["token"]
                return True
            logging.warning("Token过期重新获取...")
        except (FileExistsError, FileNotFoundError):
            logging.warning("文件不存在,重新获取Token...")
        url = "{base_url}/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
        args = {"base_url": self.base_url, "app_id": self.app_id, "app_secret": self.app_secret}
        result_token = self.request(url.format(**args), timeout=20)
        if result_token is None and result_token.status_code != 200:
            logging.error("获取Token失败...")
            return False
        if result_token.json().get("errmsg") is not None:
            logging.error("{err_msg}".format(err_msg=result_token.json().get("errmsg")))
            return False
        token_data = {
            "token": result_token.json()["access_token"],
            "expires_time": int(datetime.now().timestamp()) + 7200}
        with open(self.config_token, "w") as f:
            json.dump(token_data, f)
        logging.info("Token获取成功...")
        self.token = token_data["token"]
        return True

    def get_servers(self):
        """
        获取微信可用服务器列表，加入到本地信任的列表中
        :return:
        """
        url = "{base_url}/cgi-bin/getcallbackip?access_token={token}".format(base_url=self.base_url, token=self.token)
        result_server = self.request(url, timeout=20)
        if result_server is None and result_server.status_code != 200:
            logging.error("获取服务器列表失败...")
            return []
        logging.info("获取服务器列表成功...")
        return result_server.json()["ip_list"]

    def send_custom(self, open_id, content):
        """
        发送客服消息
        :param open_id:
        :param content:
        :return:
        """
        url = "{base_url}/cgi-bin/message/custom/send?access_token={token}".format(base_url=self.base_url,
                                                                                   token=self.token)
        data = {
            "touser": "{open_id}".format(open_id=open_id),
            "msgtype": "text",
            "text": {
                "content": "{content}".format(content=content.decode("utf-8"))
            }
        }
        result_send = self.request(url, method="post",
                                   data=bytes(json.dumps(data, ensure_ascii=False), encoding='utf-8'))
        if result_send is not None and result_send.status_code == 200 and result_send.json()["errcode"] == 0:
            # logging.info("微信消息发送成功, 时间: {time}...".format(time=datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
            return True
        logging.error("微信消息发送失败, 错误: {error} 时间: {time}...".format(error=result_send.json()["errmsg"],
                                                                   time=datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
        return False

    def nick_name_get(self, open_id):
        """
        获取用户昵称
        :param open_id:
        :return:
        """
        url = "{base_url}/cgi-bin/user/info?access_token={token}&openid={open_id}&lang=zh_CN".format(
            base_url=self.base_url, open_id=open_id, token=self.token)
        nick_result = self.request(url)
        if nick_result is None or nick_result.status_code != 200:
            logging.error("昵称获取失败...")
            return None
        return nick_result.json().get("nickname")


class StorageUser:
    def __init__(self, storage_path):
        self.storage_path = os.path.join(storage_path, "conf", "storage.db")

    def __read(self):
        try:
            with open(self.storage_path) as f:
                return json.load(f)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            logging.error("存储文件损坏或不存在...")
            return []

    def read(self):
        """
        读取绑定用户信息
        :return:
        """
        if not os.path.exists(self.storage_path) or not os.path.isfile(self.storage_path):
            logging.error("存储路径{storage_path}不存在, 无法获取用户信息...".format(storage_path=self.storage_path))
            return []
        return self.__read()

    def write(self, open_id, nick_name, email):
        """
        新增绑定用户
        :param open_id:
        :param nick_name:
        :param email:
        :return:
        """
        if not os.path.exists(os.path.dirname(self.storage_path)) or not os.path.isdir(
                os.path.dirname(self.storage_path)):
            logging.error("存储路径{storage_path}不存在...".format(storage_path=self.storage_path))
            return False
        data = self.__read()
        data.append({
            "open_id": open_id,
            "nick_name": nick_name,
            "email": email,
            "create_time": int(datetime.now().timestamp())
        })
        with open(self.storage_path, "w") as f:
            json.dump(data, f)

    def remove(self, open_id):
        """
        移除绑定用户
        :param open_id:
        :return:
        """
        if not os.path.exists(os.path.dirname(self.storage_path)) or not os.path.isdir(
                os.path.dirname(self.storage_path)):
            logging.error("存储路径{storage_path}不存在...".format(storage_path=self.storage_path))
            return None
        target_open_id = list(filter(lambda x: x["open_id"].strip() == open_id.strip(), self.read()))
        if not target_open_id:
            return None
        with open(self.storage_path, "w") as f:
            json.dump(list(filter(lambda x: x["open_id"].strip() != open_id.strip(), self.read())), f)
        return target_open_id[0]
