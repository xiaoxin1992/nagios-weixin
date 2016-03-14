#!  _*_ coding:utf-8
from requests import get, post
import datetime
from json import loads, dumps
import os
import functools


def file_check(fn):
	functools.wraps(fn)

	def check(*args, **kwargs):
		if kwargs.get('path') is None or not os.path.exists(kwargs.get('path')):
			raise FileNotFoundError("file does not exist %s" % kwargs.get('path'))
		return fn(*args, **kwargs)
	return check


@file_check
class WeiXin:
	def __init__(self, appid, secret, path):
		self.__appid = appid
		self.__secret = secret
		self.__token = None
		self.token_path = path

	@staticmethod
	def check_error(data):
		if data.get('errcode'):
			print(data)
			return False
		return True

	def save_token(self):
		date = datetime.datetime.now()
		self.__token['date'] = str(date)
		f = open(self.token_path, 'w')
		f.write(dumps(self.__token))
		f.flush()
		return self.__token['access_token']

	def get_token(self):
		token_url = '''https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s''' % (
			self.__appid, self.__secret)
		token = get(token_url, timeout=20).json()
		if self.check_error(token):
			self.__token = token
			return True
		return False

	def read_token(self):
		date = datetime.datetime.now()
		f = open(self.token_path, 'r')
		try:
			token = loads(f.readline())
		except Exception:
			return False
		if (date - datetime.datetime.strptime(token.get('date'), '%Y-%m-%d %H:%M:%S.%f')).seconds > token['expires_in']:
			return False
		return token['access_token']