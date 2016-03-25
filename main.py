from aspect.reviewProcessing import ReviewP
from aspect.sentimental import Sentiment
from aspect.aspectratings import AspectR
from reviews.trippool import TripAdvisor
from reviews.zomatopool import Zomato


class Sentient(object):
	"""docstring for Sentient"""
	def __init__(self,url,survey_id,provider):
		self.u=url
		self.sid= survey_id
		self.p= provider
	def scrap_data(self):

		if "zomato.com" in self.u:
			# self.p= "zomato"
			Zomato(self.u,self.sid).get_data()
			print("zomato")
		if "tripadvisor.com" in self.u:
			# self.p="tripadvisor"
			TripAdvisor(self.u,self.sid).get_data()
			print("tripadvisor")
		
	def run_ml(self):
		ReviewP(self.sid,self.p).run()
		Sentiment(self.sid,self.p).run()
		AspectR(self.sid,self.p).run()

	def run(self):
		self.scrap_data()
		self.run_ml()
if __name__ == '__main__':
	url= "https://www.zomato.com/ncr/purani-dilli-restaurant-zakir-nagar-new-delhi"
	survey_id="amazing"
	provider="zomato"
	Sentient(url,survey_id,provider).run()
	