# -*- coding:UTF8 -*-
from wx_lib.base import WXBase
import logging
from wx_lib.config import GetConfig
from wx_lib.base import StorageUser
import sys
import argparse
from prettytable import PrettyTable


class SendMassage(GetConfig):
    def __init__(self):
        self.root = sys.path[0]
        self.config = None

    def wx_send(self, open_id, data):
        config = self.get_config()
        if config is None:
            return False
        wx_send_obj = WXBase(config["app_id"], config["secret"], self.root)
        token = wx_send_obj.get_token()
        if token is None:
            logging.error("Token获取失败,无法发送消息...")
            return False
        return wx_send_obj.send_custom(open_id, data)

    def get_mail(self):
        storage_obj = StorageUser(self.root)
        table = PrettyTable(["邮箱", "微信昵称", "创建时间"])
        for opens_id in storage_obj.read():
            table.add_row([open_id["email"], opens_id["nick_name"], open_id["create_time"]])

    def check_mail(self, email):
        storage_obj = StorageUser(self.root)
        mails = list(filter(lambda x: x["email"].strip() == email.strip(), storage_obj.read()))
        if mails:
            return mails[0]
        return None


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(description="微信消息发送工具")
    parser.add_argument("--mail", "-m", nargs="+", help="邮箱地址")
    parser.add_argument("--content", "-c", help="消息内容")
    parser.add_argument("--list", "-l", action='store_true', help="列出绑定邮箱地址")
    args = parser.parse_args()
    wx_obj = SendMassage()
    if args.list:
        wx_obj.get_mail()
    elif args.content and args.mail:
        for mail in args.mail:
            open_id = wx_obj.check_mail(mail)
            if open_id is None:
                logging.error("邮箱: {mail}不存在,不进行消息发送".format(mail=mail))
                continue
            if wx_obj.wx_send(open_id["open_id"], args.content.encode("utf-8")):
                logging.info("{nick_name},邮箱为:{mail}发送消息成功...".format(nick_name=open_id["nick_name"], mail=mail))
    else:
        parser.print_help()