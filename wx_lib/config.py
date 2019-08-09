# -*- coding:UTF8 -*-
from wx_lib.base import WXBase
import logging
import json
import os


class GetConfig:
    def __init__(self, root):
        self.root = root

    def get_config(self):
        """
        获取微信配置文件
        :return:
        """
        config_path = os.path.join(self.root, "conf", "config.json")
        if not (os.path.exists(config_path) and os.path.isfile(config_path)):
            logging.error("配置文件不存在,　请先配置...")
            return None

        try:
            with open(config_path) as f:
                return json.load(f)
        except json.decoder.JSONDecodeError as e:
            logging.error("配置文件格式错误， 错误：{error}...".format(error=e))
            return None
