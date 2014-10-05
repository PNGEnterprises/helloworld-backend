import os
import json
import time
from flask import Flask
from flask import request
from data_handler import insert, query
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/v1/get-messages", methods=['POST'])
def get_messages():
	data = json.loads(request.data)
	try:
		latLocation = data["latLocation"]
	except:
		return '{"error":"latLocation"}'

	try:
		lonLocation = data["lonLocation"]
	except:
		return '{"error":"latLocation"}'

	try:
		messages = query(latLocation, lonLocation)
	except:
		return '{"error":"database"}'

	print messages
	return json.dumps({"error":"success", "messages":messages})

@app.route("/api/v1/post-message", methods=['POST'])
def post_message():
	data = json.loads(request.data)
	if(not("latLocation" in data.keys())):
		return '{"error":"latLocation"}'

	if(not("lonLocation" in data.keys())):
		return '{"error":"lonLocation"}'

	if(not("message" in data.keys())):
		return '{"error":"message"}'

	if(len(data["message"]) > 200):
		return '{"error":"message", "message":"Message must be 200 characters or less"}'

	timeLogged = time.time()
	if(insert(data, timeLogged)):
		return '{"error":"success"}'
	else:
		return '{"error":"database"}'

def query_stub(latLocation, lonLocation):
	return [{"latLocation":147.254,"lonLocation":87.698,"message":"Hello, World!","timeLogged":123456},{"latLocation":120.765,"lonLocation":78.123,"message":"Hello, JAKEH!","timeLogged":789045}]

def insert_stub(data, timeLogged):
	return 1;

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
