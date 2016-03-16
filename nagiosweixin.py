#  _*_ coding:utf-8
from baseweixin import WeiXin, get, post
from json import dumps, loads
import sqllite
import datetime
import sys
import os
import getopt
import ClassMail


def check_error(check_data):
	if data.get('errcode'):
		print(check_data)
		return False
	return True


def get_openid(openid_token):
	next_openid = ""
	open_list = []
	while True:
		get_oepnid_url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s" % \
			(openid_token, next_openid)
		user_openid = get(get_oepnid_url, timeout=20).json()
		openid_check = check_error(user_openid)
		if not openid_check:
			print(openid_check)
			return False
		open_list.extend(openid['data']['openid'])
		next_openid = openid.get('next_openid')
		if next_openid:
			break
	return open_list


def get_wx_server_ip(path, wx_token):
	wx_server_url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s" % wx_token
	server_list = get(wx_server_url, timeout=20).json()
	if check_error(server_list):
		with open(path, 'w') as f:
			f.write(dumps(server_list['ip_list']))
			f.flush()


def get_user_info(user_openid, user_token):
	user_info_url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % \
		(user_token, user_openid)
	re_info = get(user_info_url, timeout=20).json()
	return re_info


def send_template(send_data, send_token):
	msg_template = {
		'touser': send_data.get('touser'),
		'template_id': send_data.get('template_id'),
		'url': data.get('url'),
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
	template_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % send_token
	return post(template_url, data=dumps(msg_template).encode('utf-8')).json()


def check_user_info(email):
	db_self = sqllite.Database()
	mail_address = db_self.select(s_type="mail", data=email)
	db_self.close()
	if mail_address:
		return mail_address[0]
	return None


def send_mail(maildata, server_info):
	mail = ClassMail.EasySendmail()
	mail.host = server_info.get('smtp_server')
	mail.sender = server_info.get('mail_sender')
	mail.passwd = server_info.get("mail_password")
	mail.mail_to = maildata.get('touser')
	mail.mail_sub = maildata.get('msg_title')
	mail.content = maildata.get("msg_error")
	mail.sendmail
if __name__ == "__main__":
	path = os.path.join(os.path.dirname(sys.argv[0]), 'conf/config.json')
	if not os.path.exists(path):
		sys.exit(1)
	with open(path, 'r') as f:
		mail_data = f.read()
	try:
		config = loads(mail_data)
	except Exception as e:
		print(e)
		sys.exit(1)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:s:")
	except Exception as e:
		print(e)
		print("Usage: %s {-h help|-m mail address|-s subject}" % sys.argv[0])
		sys.exit(1)
	title = None
	msg_error = None
	msg_info = "请注意查看"
	for x in opts:
		if x[0] == '-m':
			openid = x[1]
		elif x[0] == "-s":
			title = x[1]
	msg_error = sys.stdin.read()
	if not title and not msg_error:
		print("Usage: %s {-h help|-m mail address|-s subject}" % sys.argv[0])
		sys.exit(1)
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	data = {
		'touser': openid,
		'template_id': config.get('template_id'),
		'url': '',
		'msg_title': title,
		'msg_error': msg_error,
		'time': time,
		'msg_info': msg_info
	}
	for x in openid.split(','):
		wxopenid = check_user_info(x)
		data['touser'] = x
		if not wxopenid:
			send_mail(data, config)
			sys.exit(0)
		data['touser'] = wxopenid
		nagios = WeiXin(appid=config.get('appid'), secret=config.get('secret'))
		token = nagios.read_token()
		if token:
			print("send message %s " % send_template(data, send_token=token).get('errmsg'))
	sys.exit(0)
