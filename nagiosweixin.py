#!  _*_ coding:utf-8
from baseweixin import WeiXin, get, post, file_check,dumps
import sqllite
import datetime
import sys
import getopt


def get_openid(openid_token, check_def):
	next_openid = ""
	open_list = []
	while True:
		get_oepnid_url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s" % \
			(openid_token, next_openid)
		user_openid = get(get_oepnid_url, timeout=20).json()
		openid_check = check_def.check_error(user_openid)
		if not openid_check:
			print(openid_check)
			return False
		open_list.extend(openid['data']['openid'])
		next_openid = openid.get('next_openid')
		if next_openid:
			break
	return open_list


@file_check
def create_menu(path, menu_token, menutype="add"):
	delete_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % menu_token
	if menutype == "delete":
		return get(delete_url, timeout=20).json()
	menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % menu_token
	with open(path, 'r') as f:
		menu_template = f.read()
	ret_post = post(menu_url, data=menu_template.encode('utf-8')).json()
	if nagios_send.check_error(ret_post):
		return ret_post
	return ret_post


def get_wx_server_ip(path, wx_token):
	wx_server_url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s" % wx_token
	server_list = get(wx_server_url, timeout=20).json()
	if nagios_send.check_error(server_list):
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
	return post(template_url, data=dumps(msg_template, ensure_ascii=False).encode('utf-8')).json()


def get_user_info(email):
	db_self = sqllite.Database()
	mail_address = db_self.select(s_type="mail", data=email)
	db_self.close()
	if mail_address:
		return mail_address[0]
	return None

if __name__ == "__main__":
	appid = "wxe0a7ad56e757975f"
	secret = "d4624c36b6795d1d99dcf0547af5443d"
	token_path = "./conf/token.json"
	menu_path = './conf/menu.txt'
	template_id = "6puShra9rwhBxNm12lQHj-TvFxoJbmKa_ONkemF4TV0"
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:s:c:i:")
	except Exception as e:
		print(e)
		print("Usage: %s {-h help|-m mail address|-s subject|-c content|-i prompt massage}" % sys.argv[0])
		sys.exit(1)
	title = None
	msg_error = None
	msg_info = None
	for x in opts:
		if x[0] == '-m':
			openid = get_user_info(x[1])
		elif x[0] == "-s":
			title = x[1]
		elif x[0] == "-c":
			msg_error = x[1]
		elif x[0] == "-i":
			msg_info = x[1]
	if not title and not msg_error and not msg_info:
		print("Usage: %s {-h help|-m mail address|-s subject|-c content|-i prompt massage}" % sys.argv[0])
		sys.exit(1)
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	data = {
		'touser': openid,
		'template_id': template_id,
		'url': '',
		'msg_title': title,
		'msg_error': msg_error,
		'time': time,
		'msg_info': msg_info
	}
	send_template(data, token)

