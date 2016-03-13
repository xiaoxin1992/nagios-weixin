#!  _*_ coding:utf-8
from flask import Flask, request,redirect, url_for, session
from xml.etree import cElementTree
import hashlib
import json
token = "xiaoxin"
tousername = "gh_e9f237c71fe9"



def sha1(data):
	m = hashlib.sha1()
	m.update(data.encode('utf-8'))
	return m.hexdigest()


def get_ip():
	path = "./conf/wx_server_ip.txt"
	with open(path, 'r') as f:
		data = f.read()
	return json.loads(data)
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/", methods=['GET', 'POST'])
def index():

	if request.remote_addr.strip() not in get_ip():
		return "滚犊子!"
	if request.method == "GET":
		signature = request.args.get('signature')
		echostr = request.args.get('echostr')
		timestamp = request.args.get('timestamp')
		nonce = request.args.get('nonce')
		if not echostr:
			return "滚犊子!"
		data = sorted([token, timestamp, nonce])
		if sha1(''.join(data)) == signature.strip():
			return echostr.strip()
	else:
		print("post start")
		xml_data = cElementTree.fromstring(request.stream.read())
		if xml_data.find('MsgType').text.strip() == "event" and xml_data.find('Event').text.strip() == "VIEW":
			if xml_data.find('ToUserName').text.strip() == tousername:
				url = "session/%s" % xml_data.find('FromUserName').text.strip()
				redirect(url_for(url))
		return "ok"

@app.route("/session/<openid>", methods=['GET','POST'])
def wxsession(openid):
	session['openid'] = openid
	print(session)
	return "ok"

@app.route("/install", methods=['GET', 'POST'])
def install():
	print(session)
	if request.method == "POST":
		rec = request.stream.read()
		return "h"
		#return "邮箱地址是:%s,要绑定的微信ID为: %s" % (request.form.get('mail'), session.get('openid'))
	return "<html><body><form action='' method='post'><div>邮箱地址:<input type='text' name='mail'>" \
		"<input type='submit' value='绑 定'></div></form>" \
		"</body></html>"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
