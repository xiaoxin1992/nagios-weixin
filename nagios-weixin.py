#!  _*_ coding:utf-8
from baseweixin import WeiXin, get, post, file_check,dumps


appid = "wxe0a7ad56e757975f"
secret = "d4624c36b6795d1d99dcf0547af5443d"
token_path = "./conf/token.json"
menu_path = './conf/menu.txt'

nagios_send = WeiXin(appid=appid, secret=secret, path=token_path)
token = nagios_send.read_token()
if not token:
	if not nagios_send.get_token():
		print("get token fail")
	token = nagios_send.save_token()


def get_openid(openid_token):
	next_openid = ""
	open_list = []
	while True:
		get_oepnid_url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s" % \
			(openid_token, next_openid)
		openid = get(get_oepnid_url, timeout=20).json()
		openid_check = nagios_send.check_error(openid)
		if not openid_check:
			print(openid_check)
			return False
		open_list.extend(openid['data']['openid'])
		next_openid = openid.get('next_openid')
		if next_openid:
			break
	return open_list


@file_check
def create_menu(path, menu_token):
	menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % menu_token
	with open(path, 'r') as f:
		menu_template = f.read()
	return post(menu_url, data=menu_template.encode('utf-8')).json()
def get_wx_server_ip(path, wx_token):
	wx_server_url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s" % wx_token
	server_list = get(wx_server_url, timeout=20).json()
	if nagios_send.check_error(server_list):
		with open(path, 'w') as f:
			f.write(dumps(server_list['ip_list']))
			f.flush()

print(create_menu(path=menu_path, menu_token=token))
#get_wx_server_ip(path="./conf/wx_server_ip.txt", wx_token=token)
"""

def kf_message(self, tokent, openid, message, msgtype='text'):
		send_url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % tokent
		message_template = {
			"touser": openid,
			"msgtype": msgtype,
			"text": {
				"content": message
			}
		}
		return requests.post(send_url, data=json.dump(message_template, ensure_ascii=False)).json()

"""