from flask import Flask,abort, redirect, url_for
app = Flask(__name__)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return "ok"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
