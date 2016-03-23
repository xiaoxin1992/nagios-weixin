import os
import sys
import json
import datetime
import getopt
from wx_lib import sqllite
from wx_lib import wxconfig
from wx_lib import ClassMail
from wx_lib.wx_base_class import WxBase

class Config:
	@classmethod
	def __get_config(cls, root_path):
		config_path = os.path.join(root_path, 'conf/config.json')
		if os.path.isfile(config_path) and os.path.exists(config_path):
			with open(config_path) as f:
				config_data = f.read()
			return json.loads(config_data)
		else:
			return None

	@classmethod
	def set_config(cls):
		root_path = os.path.abspath(os.path.dirname(sys.argv[0]))
		data = cls.__get_config(root_path)
		if not data:
			return False
		wxconfig.DBfile.path = os.path.join(root_path, 'conf/userinfo.db')
		wxconfig.Logpath.path = os.path.join(root_path, 'log/wx_nagios.log')
		wxconfig.Wxserverlist.path = os.path.join(root_path, 'conf/wx_server_ip.txt')
		wxconfig.Wxid.appid = data.get('appid')
		wxconfig.Wxid.secret = data.get('secret')
		wxconfig.Wxid.template_id = data.get('template_id')
		wxconfig.MailServer.smtp = data.get('smtp_server')
		wxconfig.MailServer.sender = data.get('mail_sender')
		wxconfig.MailServer.password = data.get('mail_password')

	@classmethod
	def sendmail(cls, maildata):
		mail = ClassMail.EasySendmail()
		mail.host = wxconfig.MailServer.smtp
		mail.sender = wxconfig.MailServer.sender
		mail.passwd = wxconfig.MailServer.password
		mail.mail_to = maildata.get('touser')
		mail.mail_sub = maildata.get('msg_title')
		mail.content = maildata.get("msg_error")
		mail.sendmail


def send_message(msg_title, msg_errorinfo, msg_openid):
	Config.set_config()
	msg_info = "请注意查看"
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	data = {
		'touser': msg_openid,
		'template_id': wxconfig.Wxid.template_id,
		'url': '',
		'msg_title': msg_title,
		'msg_error': msg_errorinfo,
		'time': time,
		'msg_info': msg_info
	}
	db_self = sqllite.Database()
	try:
		for user_id in openid.split(','):
			mail_address = db_self.select(s_type="mail", data=user_id)
			if mail_address:
				data['touser'] = mail_address[0]
				wx_object = WxBase()
				wx_object.readtoken()
				wx_object.send_template(data)
			else:
				data['touser'] = user_id
				Config.sendmail(maildata=data)
	finally:
		db_self.close()


if __name__ == "__main__":
	title = None
	openid = None
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:s:")
	except Exception as e:
		print(e)
		print("Usage: %s {-h help|-m mail address|-s subject}" % sys.argv[0])
		sys.exit(1)
	for x in opts:
		if x[0] == '-m':
			openid = x[1]
		elif x[0] == "-s":
			title = x[1]
		elif x[0] == "-h":
			print("Usage: %s {-h help|-m mail address|-s subject}" % sys.argv[0])
			sys.exit(0)
	try:
		msg_error = sys.stdin.read()
	except KeyboardInterrupt:
		sys.exit(0)
	if title is None or not msg_error or openid is None:
		print("Usage: %s {-h help|-m mail address|-s subject}" % sys.argv[0])
		sys.exit(1)
	send_message(msg_title=title, msg_errorinfo=msg_error, msg_openid=openid)

