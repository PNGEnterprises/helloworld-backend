import os
import json
from flask import Flask
from flask import request
import time
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

	message = getFromDatabase(latLocation, lonLocation)
	return message

@app.route("/api/v1/post-message", methods=['POST'])
def post_message():
	data = json.loads(request.data)
	try:
		latLocation = data["latLocation"]
	except:
		return '{"error":"latLocation"}'

	try:
		lonLocation = data["lonLocation"]
	except:
		return '{"error":"lonLocation"}'

	try:
		message = data["message"]
	except:
		return '{"error":"message"}'

	if(len(message) > 200):
		return '{"error":"message", "message":"Message must be 200 characters or less"}'

	timeLogged = int(time.time())
	if(writeToDatabase(latLocation, lonLocation, message, timeLogged)):
		return '{"error":"success"}'
	else:
		return '{"error":"database"}'

def getFromDatabase(latLocation, lonLocation):
	return '{"latLocation":147.254,"lonLocation":87.698,"message":"Hello, World!","timeLogged":123456}'

def writeToDatabase(latLocation, lonLocation, message, timeLogged):
	return 1;

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
