#  _*_ coding:utf-8
from requests import get, post
import datetime
import datetime
import sqllite


class WeiXin:
	def __init__(self, appid, secret):
		self.__appid = appid
		self.__secret = secret
		self.__token = {}

	@staticmethod
	def check_error(data):
		if data.get('errcode'):
			print(data)
			return False
		return True

	def get_token(self):
		db_data = sqllite.Database()
		token_url = '''https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s''' % (
			self.__appid, self.__secret)
		access_token = get(token_url, timeout=20).json()
		if self.check_error(access_token):
			self.__token = {
				'token': access_token['access_token'],
				'expire': access_token['expires_in'],
				'date': str(datetime.datetime.now())
			}
			db_data.delete(tname_type="wx_token")
			re_status = db_data.inster(s_type="wx_token", data=self.__token)
			db_data.close()
			if re_status:
				return True
		return False

	def read_token(self):
		new_time = datetime.datetime.now()
		db_data = sqllite.Database()
		data = db_data.select(s_type="wx_token")
		if not data:
			if not self.get_token():
				return False
		if data.get('date'):
			diff_time_day = (new_time - datetime.datetime.strptime(data.get('date'), '%Y-%m-%d %H:%M:%S.%f')).days
			diff_time_seconds = (new_time - datetime.datetime.strptime(data.get('date'), '%Y-%m-%d %H:%M:%S.%f')).seconds
			diff_seconds = diff_time_day * 24 * 3600 + diff_time_seconds
			if diff_seconds > int(data.get('expire')):
				if not self.get_token():
					return False
		if not self.__token.get('token'):
			self.__token['token'] = data.get('token').strip()
		return self.__token.get('token')
