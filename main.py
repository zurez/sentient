from aspect.reviewProcessing import ReviewP
from aspect.sentimental import Sentiment
from aspect.aspectratings import AspectR
from reviews.trippool import TripAdvisor
from reviews.zomatopool import Zomato
from reviews.nlp import WordCloud
class Sentient(object):
	"""docstring for Sentient"""
	def __init__(self,url,survey_id,provider):
		self.u=url
		self.sid= survey_id
		self.p= provider
	def scrap_data(self):
		print("************************")
		if "zomato.com" in self.u or self.p=="zomato":
			# self.p= "zomato"
			Zomato(self.u,self.sid).get_data()
			print("zomato")
		if "tripadvisor" in self.u:
			# self.p="tripadvisor"
			TripAdvisor(self.u,self.sid).get_data()
			print("tripadvisor")
	def wordcloud(self):
		WordCloud(self.sid,self.p).wc()
	def run_ml(self):
		ReviewP(self.sid,self.p).run()
		Sentiment(self.sid,self.p).run()
		AspectR(self.sid,self.p).run()
	def run(self):
		self.scrap_data()
		self.wordcloud()
		self.run_ml()
		#SOMETHING IS VERY WRONG!!kyaaa?DID YOU JUST NOT SEE I DISABLED WORDCLOUD AND ML
		#THEY SHOULD NOT BE RUN. ALSO I DONT SEE STARS
if __name__ == '__main__':
	# url= "https://www.zomato.com/ncr/purani-dilli-restaurant-zakir-nagar-new-delhi"
	url="https://www.zomato.com/ncr/chaayos-sector-38-noida"
	#survey_id="or8Q4A1xDoXr5ybmDmf"
	survey_id="test124"
	provider="zomato"
	Sentient(url,survey_id,provider).run()
	