from mongoengine import *
# Connect to Database
#lazy connection
connect("testdemo")
class Reviews(Document):
	"""docstring for Reviews"""
	
	provider=StringField()
	survey_id=StringField()
	rating=StringField()
	review=StringField()
