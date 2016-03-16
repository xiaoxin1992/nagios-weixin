import sqlite3
import os
import sys


class Database(object):
	def __init__(self):
		self.path = os.path.join(os.path.dirname(sys.argv[0]), 'conf/userinfo.db')
		self.conn = sqlite3.connect(self.path)
		self.c = self.conn.cursor()
		self.c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
		self.table_name = [x[0] for x in self.c.fetchall()]
		if 'wxid_to_mail' not in self.table_name:
			self.c.execute("CREATE TABLE wxid_to_mail(wxid char(128),mail char(128))")
		elif 'wx_token' not in self.table_name:
			self.c.execute("CREATE TABLE wx_token(token char(256),expire char(128),date char(128))")

	def select(self, s_type, data=None):
		if s_type.strip() == "wxid":
			self.c.execute("SELECT mail FROM wxid_to_mail where wxid='%s'" % data)
		elif s_type.strip() == "mail":
			self.c.execute("SELECT wxid FROM wxid_to_mail where mail='%s'" % data)
		elif s_type.strip() == "wx_token":
			token_data = {}
			self.c.execute("SELECT * FROM wx_token")
			for x in self.c.fetchall():
				token_data['token'] = x[0]
				token_data['expire'] = x[1]
				token_data['date'] = x[2]
			return token_data
		return [x[0] for x in self.c.fetchall()]

	def inster(self, wxid=None, mail=None, data=None, s_type='mail'):
		if s_type == "mail":
			self.c.execute("INSERT INTO wxid_to_mail VALUES ('%s','%s')" % (wxid, mail))
		elif s_type == "wx_token":
			self.c.execute(
				"INSERT INTO wx_token VALUES ('%s','%s','%s')" % (
					data.get('token'), data.get('expire'), data.get('date')
				)
			)
		else:
			return False
		if not self.conn.commit():
			return True
		return False

	def delete(self, tname_type='wxid', wxid=None):
		if tname_type.strip() == 'wxid' and wxid:
			self.c.execute("delete from wxid_to_mail where wxid = '%s'" % wxid)
			if not self.conn.commit():
				return True
			return False
		elif tname_type.strip() == 'wx_token':
			self.c.execute("delete from wx_token")
			if not self.conn.commit():
				return True
			return False

	def update(self, rowstype, data):
		if rowstype.strip() == "wxid" and data:
			self.c.execute("update wxid_to_mail set wxid='%s'" % data)
		elif rowstype.strip() == "mail" and data:
			self.c.execute("update wxid_to_mail set mail='%s'" % data)
		elif rowstype.strip == "wx_token":
			return False
		else:
			return False
		if not self.conn.commit():
			return True
		return False

	def close(self):
		self.conn.close()
