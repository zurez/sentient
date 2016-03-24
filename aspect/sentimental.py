import csv
from textblob import TextBlob
import os

os.chdir('..')
os.chdir('..')
filename = "Data/annotated_sentences_chi_final.csv"
def get_sentiment(text):
	blob = TextBlob(text)
	sentence_sentiment = blob.sentences[0].sentiment.polarity
	if sentence_sentiment > 0:
		return "Positive"
	if sentence_sentiment == 0:
		return "Neutral"
	if sentence_sentiment < 0:
		return "Negative"

data = []
with open(filename, "rt") as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		data.append(row)

number_of_sentences = len(data)

with open("Data/sentimentalreviews.csv", "w") as out_file:
	writer = csv.writer(out_file)

	for i in range(1, number_of_sentences):
		sentence = data[i][3]
		sentiment = get_sentiment(sentence)
		line = data[i]
		line.append(sentiment)
		writer.writerow(line)