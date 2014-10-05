from install import Message
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, time
from dateutil import parser

engine = create_engine("postgres://postgres:time4login@104.131.73.180/helloworld")
Session = sessionmaker(bind=engine)

# Adds a new message to the database
# params encapsulates all fields necessary for the message
def insert(params, time):
    session = Session()

    expiration = parser.parse(params['expiration'])
    start      = parser.parse(params['start'])
    start      = time(start.hour, start.minute, start.second, start.microsecond)
    end        = parser.parse(params['end'])
    end        = time(end.hour, end.minute, end.second, end.microsecond)

    message = Message()
    try:
        message.location = func.ST_MakePoint(params['lonLocation'], params['latLocation'])
        message.message = params['message']
        message.timeLogged = time
        message.expireTime = expiration
        message.beginTime = start
        message.endTime = end
        message.daysVisible = params['days']
        message.requiredMessageId = params['requiredId']
    except:
        return false

    try:
        session.add(message)
        session.commit()
    except:
        return false

    return true


# Queries for a list of messages that are
# within the specified radius of the provided
# lat and lng (radius is in meters?)
def query(lat, lng):
    radius = 25   # 25 meter radius
    pass
