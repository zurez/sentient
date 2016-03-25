import csv
import os
from aspect.models.model import Aspect,Reviews,SentR
# from mongoengine import *
# class Reviews(Document):
# 	pass


def aspect_rating(review_rows, aspect_rows, overall):
	positive_rows = [row for row in aspect_rows if row[2] == 'Positive']
	negative_rows = [row for row in aspect_rows if row[2] == 'Negative']

	if len(positive_rows) == len(negative_rows):
		x = (len(positive_rows) + len(negative_rows))*float(overall)/len(review_rows)
		y = (x + 10)/5

	if len(positive_rows) > len(negative_rows):
		diff = len(positive_rows) - len(negative_rows)
		x = (diff*len(review_rows))/(float(overall) * (len(positive_rows) + len(negative_rows)))
		y = 3 + 2*x/5

	if len(positive_rows) < len(negative_rows):
		diff = len(negative_rows) - len(positive_rows)
		x = (diff*len(review_rows))/(float(overall) * (len(positive_rows) + len(negative_rows)))
		y = 2*x/5

	return y


# os.chdir('..')
# os.chdir('..')
# filename = "Data/sentimentalreviews.csv"
class AspectR(object):
	"""docstring for AspectR"""
	def __init__(self,survey_id,provider):
		self.sid=survey_id
		self.p=provider
	def run(self):
		data = []
		spamreader=SentR.objects(survey_id=self.sid)
		# a= spamreader.line
		# reviews= 
		# with open(filename, "rt") as csvfile:
		# 	spamreader = csv.reader(csvfile)
		for row in spamreader:
			print("row",row)
			aspect = row.line[2]
			review_ID = row.line[1]
			polarity = row.line[5]
			data_line = [review_ID, aspect, polarity]
			data.append(data_line)
		# print(data)

		overall_ratings = []
		spamreader=Reviews.objects(survey_id=self.sid)
		# with open('Data/reviews.csv', "rt") as csvfile:
		# 	spamreader = csv.reader(csvfile)
		for row in spamreader:
			# print(row.rating)
			overall_ratings.append(float(row.rating))

		last_review_ID = max(list(map(int,[row[0] for row in data])))
		for review_ID in range(1, last_review_ID):

			review_rows = [row for row in data if row[0] == str(review_ID)]

			food_rows = [row for row in review_rows if row[1] == '0']
			service_rows = [row for row in review_rows if row[1] == '1']
			price_rows = [row for row in review_rows if row[1] == '2']
			neutral_rows = [row for row in review_rows if row[1] == '-1']

			overall = overall_ratings[review_ID]

			if len(review_rows) !=0 :
				AR_food = aspect_rating(review_rows, food_rows, overall)
				AR_service = aspect_rating(review_rows, service_rows, overall)
				AR_price = aspect_rating(review_rows, price_rows, overall)
			else :
				AR_food = overall
				AR_service = overall
				AR_price = overall
			
			# OUTPUT
			# print (review_rows)
			# print ("Food: ", AR_food, " Service: ", AR_service, " Price: ", AR_price)
			# print ("Overall", overall)
			r= Aspect(sector="food",provider=self.p,survey_id=self.sid,food=str(AR_food),service=str(AR_service),price=str(AR_price),overall=str(overall)).save()
			print("Aspect Rating Done")
# 	[['1', '1', 'Positive']]
# Food:  2.0  Service:  3.088888888888889  Price:  2.0
# Overall 4.5
