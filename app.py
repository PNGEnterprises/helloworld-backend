import os
import json
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/v1/get-message", methods=['POST'])
def get_message():
	data = json.loads(request.data)
	print data
	return str(data["latLocation"])

@app.route("/api/v1/post-message", methods=['POST'])
def post_message():
	return "You posted a message"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
