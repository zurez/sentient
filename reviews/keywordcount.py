from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class KeywordCount(object):
	def __init__(self, stop_words_path):
		self.stop_words_path = stop_words_path
		stopwords_file = open(stop_words_path, 'r')
		self.stopwords_list = stopwords_file.read().split('\n')
		# self.__stop_words_pattern = build_stop_word_regex(stop_words_path)
	

	def run(self, text):
		cv = CountVectorizer(min_df=0, stop_words=self.stopwords_list, max_features=20, analyzer = 'word', ngram_range = (1,4))
		# try:
		counts = cv.fit_transform([text]).toarray().ravel()
		# print (type(counts))
		words = np.array(cv.get_feature_names()) 

		# except ValueError:
		# 	counts = ['0']
		# 	words = ['null']
		# 	pass

		
		# normalize
		counts = counts / float(counts.max())
		final = []
		for i in range(0, len(counts)):
			final.append((words[i], counts[i]))
		return final
