#!  _*_ coding:utf-8
from flask import Flask, request, make_response
from xml.etree import cElementTree
import hashlib
import json
import time
import sys
token = "xiaoxin"


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
		msg = """<xml>
<ToUserName><![CDATA[%(openid)s]]></ToUserName>
<FromUserName><![CDATA[%(devid)s]]></FromUserName>
<CreateTime>%(time)s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%(content)s]]></Content>
</xml>"""
		xml_data = cElementTree.fromstring(request.stream.read())
		msgtype = xml_data.find("MsgType").text
		openid = xml_data.find("FromUserName").text
		fromusername = xml_data.find("ToUserName").text
		now_time = str(time.time())
		if msgtype.strip() == "event":
			if xml_data.find("Event").text.strip() == "subscribe":
				content = """欢迎关注运维微信,请直接回复邮箱地址绑定"""
				return make_response(msg % {'openid': openid, 'devid': fromusername, 'time': now_time, 'content': content})
		return "ok"
		"""
		openid = xml_data.find("FromUserName").text

		content = xml_data.find("Content").text
		if msgtype != "text":
			return "fail"
		print(openid)
		print(msgtype)
		print(content)
		"""




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
