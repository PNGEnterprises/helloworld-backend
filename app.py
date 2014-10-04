import os
import json
from flask import Flask
from flask import request
from datetime import datetime
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

	timeLogged = datetime.utcnow()
	if(writeToDatabase(latLocation, lonLocation, message, timeLogged)):
		return '{"error":"success"}'
	else:
		return '{"error":"database"}'

def writeToDatabase(latLocation, lonLocation, message, timeLogged):
	return 0;

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
