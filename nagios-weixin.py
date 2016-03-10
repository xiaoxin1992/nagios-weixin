from baseweixin import WeiXin

appid = "wxe0a7ad56e757975f"
secret = "d4624c36b6795d1d99dcf0547af5443d"
nagios_send = WeiXin(appid=appid, secret=secret)
token = nagios_send.read_token(path="./token.json")

if not token:
	if not nagios_send.get_token():
		print("get token fail")
	nagios_send.save_token()



def get_openid():


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
a = WeiXin('wxe0a7ad56e757975f', 'd4624c36b6795d1d99dcf0547af5443d')
a.get_token()
#a.save_token("./token.json")
print(a.read_token(path="./token.json"))
"""