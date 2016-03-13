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
		print(xml_data)




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
