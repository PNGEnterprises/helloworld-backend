import os
import json
from flask import Flask
from flask import request
from datetime import datetime
from sqlalchemy import func
from data_handler import query
from data_handler import insert
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/v1/get-message", methods=['POST'])
def get_message():
	data = json.loads(request.data)
	try:
		latLocation = data["latLocation"]
	except:
		return '{"error":"latLocation"}'

	try:
		lonLocation = data["lonLocation"]
	except:
		return '{"error":"latLocation"}'

	message = query(latLocation, lonLocation)
	return json.dumps(message)

@app.route("/api/v1/post-message", methods=['POST'])
def post_message():
	data = json.loads(request.data)
	if(not("latLocation" in data.keys())):
		return '{"error":"latLocation"}'

	if(not("lonLocation" in data.keys())):
		return '{"error":"lonLocation"}'

	if(not("message" in data.keys())):
		return '{"error":"message"}'

	if(len(message) > 200):
		return '{"error":"message", "message":"Message must be 200 characters or less"}'

	timeLogged = datetime.utcnow()
	if(insert(data, timeLogged)):
		return '{"error":"success"}'
	else:
		return '{"error":"database"}'

def query(latLocation, lonLocation):
	return [{"latLocation":147.254,"lonLocation":87.698,"message":"Hello, World!","timeLogged":123456},{"latLocation":120.765,"lonLocation":78.123,"message":"Hello, JAKEH!","timeLogged":789045}]

def insert(latLocation, lonLocation, message, timeLogged):
	return 1;

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
