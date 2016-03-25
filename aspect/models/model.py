#!/usr/bin/env python
from mongoengine import *
# Connect to Database
#lazy connection
connect("qwer")
class Aspect(Document):
	"""docstring for Aspect"""
	sector=StringField()
	food=StringField()
	service=StringField()
	price=StringField()
	overall=StringField()
	survey_id=StringField()
	provider=StringField()
class Reviews(Document):
	"""docstring for Reviews"""
	provider=StringField()
	survey_id=StringField()
	rating=StringField()
	review=StringField()
class ChiFinal(Document):
	data=ListField()
	survey_id=StringField()
	provider=StringField()
class ExpKeywords(Document):
	"""ExpendedAspectKeywords"""
	pass
class SentR(Document):
	"""docstring for Sentimental Reviews"""
	# sentence=StringField()
	# sentiment=StringField()
	line=ListField()
	survey_id=StringField()
	provider=StringField()

		
	
		
# for i in Aspect.objects():
# 	print(i.service)