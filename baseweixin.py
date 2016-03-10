import requests
import datetime
import json
import os
import functools


def file_check(fn):
	functools.wraps(fn)

	def check(*args,**kwargs):
		if kwargs.get('path') is None or not os.path.exists(kwargs.get('path')):
			raise FileNotFoundError("file does not exist %s" % kwargs.get('path'))
		return fn(*args, **kwargs)
	return check


class WeiXin:
	def __init__(self, appid, secret):
		self.__appid = appid
		self.__secret = secret
		self.__token = None

	def check_error(self, data):
		if data.get('errcode'):
			print(data)
			return False
		return True

	def save_token(self, save_path):
		date = datetime.datetime.now()
		self.__token['date'] = str(date)
		f = open(save_path, 'w')
		f.write(json.dumps(self.__token))
		f.flush()
		return self.__tokenp['access_token']

	def get_token(self):
		token_url = '''https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s''' % (
			self.__appid, self.__secret)
		token = requests.get(token_url, timeout=20).json()
		if self.check_error(token):
			self.__token = token
			return True
		return False

	@file_check
	def read_token(self, path):
		date = datetime.datetime.now()
		f = open(path, 'r')
		try:
			token = json.loads(f.readline())
		except Exception:
			return False
		if (date - datetime.datetime.strptime(token.get('date'), '%Y-%m-%d %H:%M:%S.%f')).seconds > token['expires_in']:
			return False
		return token['access_token']
