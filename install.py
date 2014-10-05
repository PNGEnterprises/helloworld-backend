from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

import os

engine = create_engine(os.environ.get("HEROKU_POSTGRESQL_CHARCOAL_URL", "postgres://pdvxuefuwwxotp:6p_RAHUaJa4ClWP20EGsHbISJe@ec2-54-243-42-236.compute-1.amazonaws.com:5432/d62ri4ks7m4d6"), echo=True)

Base = declarative_base()

class Message(Base):
	__tablename__ = 'messages'

	#basic fields
	id = Column(Integer, primary_key=True)
	location = Column(Geometry('POINT'))
	message = Column(String, nullable=False)
	timeLogged = Column(DateTime, nullable=False)
	
	#timed duration fields
	expireTime = Column(DateTime)
	
	#recurring times
	beginTime = Column(Time)
	endTime = Column(Time)
	daysVisible = Column(Integer)
	
	#unlocks
	requiredMessageId = Column(Integer, ForeignKey("messages.id"))
	requireMessage = relationship("Message")

	def __repr__(self):
		return "<Message([%s] at (%f, %f) '%s'>" % (
			(str(self.id) if self.id else 'None'), self.latLocation, self.lonLocation, self.message)
