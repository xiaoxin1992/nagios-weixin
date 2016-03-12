#!  _*_ coding:utf-8
from flask import Flask, make_response,request
import xml.etree.cElementTree as ET
import hashlib
import json
app = Flask(__name__)
token = "xiaoxin"


def sha1(data):
	m = hashlib.sha1()
	m.update(data.encode('utf-8'))
	return m.hexdigest()


def get_ip():
	path = "./conf/wx_server_ip.txt"
	with open(path,'r') as f:
		data = f.readlines()
	return data


@app.route("/")
def index():
	print(request.remote_addr)
	if request.remote_addr.strip() not in get_ip():
		print(request.remote_addr)
		print("ok")
		return "滚犊子!"
	else:
		if request.method == "GET":
			signature = request.args.get('signature')
			echostr = request.args.get('echostr')
			timestamp = request.args.get('timestamp')
			nonce = request.args.get('nonce')
			data = [token, timestamp, nonce]

			if None is data:
				data.sort()
		if signature:
			if sha1(''.join(data)) == signature.strip():
				return echostr.strip()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
