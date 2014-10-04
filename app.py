import os

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/v1/get-message", methods=['POST'])
def get_message():
	return "You got a message"

@app.route("/api/v1/post-message", methods=['POST'])
def post_message():
	return "You posted a message"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
