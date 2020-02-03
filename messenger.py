from flask import Flask

app = Flask(__name__)


@app.route('/messages')
def handle_messages():
	return 'messages handled'
