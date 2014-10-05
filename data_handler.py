from install import Message
from sqlalchemy import create_engine, func, or_, and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime, time, date
from dateutil import parser

engine = create_engine("postgres://postgres:time4login@104.131.73.180/helloworld")
Session = sessionmaker(bind=engine)

# Adds a new message to the database
# params encapsulates all fields necessary for the message
def insert(params, time):
    session = Session()

    if "expiration" in params.keys():
        expiration = parser.parse(params['expiration'])
    else:
        expiration = None

    if "start" in params.keys() and "end" in params.keys():
        start      = parser.parse(params['start'])
        start      = time(start.hour, start.minute, start.second, start.microsecond)
        end        = parser.parse(params['end'])
        end        = time(end.hour, end.minute, end.second, end.microsecond)
    else:
        start = None
        end = None

    if "days" in params.keys():
        days = params["days"]
    else:
        days = None

    if "requiredId" in params.keys():
        requiredId = params["requiredId"]
    else:
        requiredId = None

    message = Message()
    try:
        message.location = func.ST_SetSRID(func.ST_MakePoint(params['lonLocation'], params['latLocation']), 4326)
        message.message = params['message']
        message.timeLogged = time
        message.expireTime = expiration
        message.beginTime = start
        message.endTime = end
        message.daysVisible = days
        message.requiredMessageId = requiredId
    except:
        return False

    try:
        session.add(message)
        session.commit()
    except:
        return False

    return True


# Queries for a list of messages that are
# within the specified radius of the provided
# lat and lng (radius is in meters?)
def query(lat, lng):
    radius = 0.000225   #0.000225 approx 25 meter radius, no adjustment for distortions in lat/lng
    session = Session()

    found = []
    now = datetime.utcnow()
    timeOfDay = time(now.hour, now.minute, now.second, now.microsecond)
    dayOfWeek = date(now.year, now.month, now.day).weekday()
    dayOfWeekMask = 1<<dayOfWeek

    try:
        center = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        found = session.query(Message.id,
                func.ST_Y(Message.location),
                func.ST_X(Message.location),
                Message.message,
                Message.timeLogged,
                Message.expireTime,
                Message.beginTime,
                Message.endTime,
                Message.daysVisible).filter(
                func.ST_DWithin(Message.location, center, 0.000225))

        # delete expired messages
        expired = found.filter(Message.expireTime != None).filter(Message.expireTime < now)
        for e in expired:
            session.delete(e)
        session.commit()
        found = found.filter(or_(Message.expireTime >= now, Message.expireTime == None))

        # ensure time of day is correct
        found = found.filter(or_(Message.beginTime == None, and_(Message.beginTime < timeOfDay, Message.endTime > timeOfDay)))

        # ensure day is correct
        found = found.filter(or_(Message.daysVisible == None, (Message.daysVisible.op('&')(dayOfWeekMask)) != 0))

        found = found.all()
    except:
        raise Exception("Error querying database.")

    return found

