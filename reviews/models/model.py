#!/usr/bin/env python
from mongoengine import *
# Connect to Database
#lazy connection
connect("qwer")
class Reviews(Document):
	"""docstring for Reviews"""
	
	provider=StringField()
	survey_id=StringField()
	rating=StringField()
	review=StringField()
class Scraped(Document):
	provider=StringField()
	survey_id=StringField()
	status=StringField()
	# Maybe a time field?