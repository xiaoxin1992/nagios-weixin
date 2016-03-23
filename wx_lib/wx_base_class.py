# -*- coding: utf-8 -*-
from requests import get, post
from wx_lib import log_write
from wx_lib import sqllite
from wx_lib.wxconfig import Wxid
import datetime
import json


class WxBase:
	def __init__(self):
		self.__appid = Wxid.appid
		self.__secret = Wxid.secret
		self.__token = None

	@staticmethod
	def check_request(data):
		if data.get('errcode'):
			return False
		return True

	def __get_token(self):
		token_url = '''https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s''' \
			% (self.__appid, self.__secret)
		result_token = get(token_url, timeout=20).json()
		if not self.check_request(result_token):
			log_write.log(result_token)
			return False
		self.__token = {
			'token': result_token['access_token'],
			'expire': result_token['expires_in'],
			'date': str(datetime.datetime.now())
		}
		add_token = sqllite.Database()
		add_token.inster(s_type="wx_token", data=self.__token)
		add_token.close()
		self.__token = result_token['access_token']
		return True

	def readtoken(self):
		new_time = datetime.datetime.now()
		db_data = sqllite.Database()
		data = db_data.select(s_type="wx_token")
		if not data:
			if not self.__get_token():
				return False
		diff_time_day = (new_time - datetime.datetime.strptime(data.get('date'), '%Y-%m-%d %H:%M:%S.%f')).days
		diff_time_seconds = (new_time - datetime.datetime.strptime(data.get('date'), '%Y-%m-%d %H:%M:%S.%f')).seconds
		diff_seconds = diff_time_day * 24 * 3600 + diff_time_seconds
		if diff_seconds > int(data.get('expire')):
			if not self.__get_token():
				return False
			return self.__token
		self.__token = data.get('token')
		return self.__token

	def get_wx_server_ip(self, path):
		print(self.__token)
		wx_server_url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s" % self.__token
		server_list = get(wx_server_url, timeout=20).json()
		print(server_list)
		if self.check_request(server_list):
			with open(path, 'w') as f:
				f.write(json.dumps(server_list['ip_list']))
				f.flush()
		return None

	def send_template(self, send_data):
		msg_template = {
			'touser': send_data.get('touser'),
			'template_id': send_data.get('template_id'),
			'url': send_data.get('url'),
			"data": {
				"first": {
					"value": send_data.get('msg_title'),
					"color": "#173177"
				},
				"performance": {
					"value": send_data.get('msg_error'),
					"color": "#FF0033"
				},
				'time': {
					"value": send_data.get('time'),
					"color": "#FF0033"
				},
				"remark": {
					"value": send_data.get('msg_info'),
					"color": "#173177"
				}
			}
		}
		template_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % self.__token
		result_send = post(template_url, data=json.dumps(msg_template).encode('utf-8')).json()
		log_write.log(result_send)
