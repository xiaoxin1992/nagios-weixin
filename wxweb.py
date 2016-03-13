#!  _*_ coding:utf-8
from flask import Flask, make_response,request
import xml.etree.cElementTree as ET
import hashlib
import json
token = "xiaoxin"
tousername = "gh_e9f237c71fe9"
openid = None


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


@app.route("/", methods=['GET'])
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
		xml_data = ET.fromstring(request.stream.read())
		if xml_data.find('MsgType').text.strip() == "event" and  xml_data.find('Event').text.strip() == "VIEW":
			if xml_data.find('ToUserName').text.strip() == tousername:
				openid = xml_data.find('FromUserName').text.strip()
		return "ok"


@app.route("/install", methods=['GET', 'POST'])
def install():
	if request.method == "POST":
		rec = request.stream.read()
		print(rec)
		return request.form.get('mail')
	return "<html><body><form action='' method='post'><div>邮箱地址:<input type='text' name='mail'>" \
		"<input type='submit' value='绑 定'></div></form>" \
		"</body></html>"
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
