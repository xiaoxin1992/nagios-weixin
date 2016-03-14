import  sqlite3


class Database(object):
	def __init__(self):
		self.conn = sqlite3.connect("./conf/userinfo.db")
		self.c = self.conn.cursor()
		self.c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
		if 'wxid_to_mail' not in [x[0] for x in self.c.fetchall()]:
			self.c.execute("CREATE TABLE wxid_to_mail(wxid char(128),mail char(128))")

	def select(self, s_type, data):
		if s_type.strip() == "wxid":
			self.c.execute("SELECT mail FROM wxid_to_mail where wxid='%s'" % data)
		elif s_type.strip() == "mail":
			self.c.execute("SELECT wxid FROM wxid_to_mail where mail='%s'" % data)
		return [x[0] for x in self.c.fetchall()]

	def inster(self, wxid, mail):
		self.c.execute("INSERT INTO wxid_to_mail VALUES ('%s','%s')" % (wxid, mail))
		if not self.conn.commit():
			return True
		return False

	def delete(self, wxid):
		self.c.execute("delete from wxid_to_mail where wxid = '%s'" % wxid)
		if not self.conn.commit():
			return True
		return False

	def update(self, rowstype, data):
		if rowstype.strip() == "wxid" and data:
			self.c.execute("update wxid_to_mail set wxid='%s'" % data)
		elif rowstype.strip() == "mail" and data:
			self.c.execute("update wxid_to_mail set mail='%s'" % data)
		else:
			return False
		if not self.conn.commit():
			return True
		return False

	def close(self):
		self.conn.close()

#{'test': 'xiaoxin', 'mail.c': '123', 'mailqq.com': '1234'}
#a = Database()
#a.delete('1234')
#print(a.select())
#print(a.update(rowstype='wxid', data='adcada12341'))

#print(a.select())
