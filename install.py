from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Time, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

import os

engine = create_engine("postgres://postgres:time4login@104.131.73.180/helloworld", echo=True)

Base = declarative_base()

class Message(Base):
	__tablename__ = 'messages'

	#basic fields
	id = Column(Integer, primary_key=True)
	location = Column(Geometry(geometry_type='POINT', srid=4326))
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
		return "<Message([%s] '%s'>" % (
			(str(self.id) if self.id else 'None'), self.message)
