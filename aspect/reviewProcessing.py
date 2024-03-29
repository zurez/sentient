from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import nltk
from aspect import aspectSegmenter 
import pandas as pd
import re
import os
from aspect.models.model import Aspect,Reviews,ChiFinal
# nltk.download('')

lemmatizer = nltk.WordNetLemmatizer()

# Import stop words just once
# stops = set(stopwords.words("english_stop_lara"))  #Not able to find the file. Using the normal corpus ~Zurez
stops= set(stopwords.words("english"))

# Indexed Vocabulary
m_vocabulary = dict()

# Contains parsed reviews (create sentences)
m_sentences = []

q_sentences = []

# This class structure holds a Token as word, 
# lemma and POS
class Token(object):
    def __init__(self, word, lemma, pos):
        self.word = word
        self.lemma = lemma
        self.pos = pos

# This class structure holds a Sentence as list
# of token objects, review ID, rating, and aspect ID   
class Sentence(object):
    def __init__(self, rid, rating, ttoken):
        self.rid = rid
        self.rating = rating
        self.ttoken = ttoken 
        self.aspectID = -1

# This function does the following:
# 1. Use NLTK to Tokenize the reviews and create sentences
# 2. Apply POS Tagger, Lemma and regular expression constraints
# 3. Expand the vocabulary per sentences        
def loadReviewAndProcess(survey_id):
    # Loading Reviews in a data frame
    # df = pd.read_csv(filename)
    reviews= Reviews.objects(survey_id=survey_id)
    # num_reviews = len(df)
    # Adding ID column to existing data frame
    # df['RID'] = range(1, num_reviews + 1)
    # reviews = df["review"]    
    rid = 0
    # print(df["review"])
    # return "finish"
    qualified_sentences = []

    print ('processing raw reviews ID:'),
    for review in reviews:
        sentences = sent_tokenize(review.review)
        m_stns = []

        

        for sentence in sentences:
            # print (sentence)
            tokens = word_tokenize(sentence)
            # discard too short sentences
            if (tokens is not None) and (len(tokens)>2):
                stn = addSentences(tokens, pos_tag(tokens), getLemma(tokens), stops)
                # print (stn)
                # print("Zurez",df['RID'][rid])
                # print(review.rating)
                m_stns.append(Sentence(rid+1, review.rating, stn))

                qualified_sentences.append(sentence)

        m_sentences.extend(m_stns)        
        # Create Indexed Vocabulary
        expandVocabulary(m_stns)    
        rid += 1
        if rid%100 == 0:
            print ('#',rid)
    print ('')        
    print ('Finished Loading reviews' ) 
    # print (qualified_sentences)
    return qualified_sentences                       

# Expand Vocabulary per sentences. Vocabulary is
# a dictionary containing key as unique words and 
# assigned values as there IDs    
def expandVocabulary(m_sentences):
    for stn in m_sentences:
        for tkn in stn.ttoken:
            if (tkn.lemma in m_vocabulary) == False:
                    m_vocabulary[tkn.lemma] = len(m_vocabulary)    

# Apply POS Tagger Constraints and create sentences
# as a list of Token objects                    
def addSentences(tokens, tagged_words, lemma, stops):
    stn = []
    for i in range(len(tokens)):  
        if ((tagged_words[i][1] is not "DT") and \
            (tagged_words[i][1] is not "IN") and \
            (tagged_words[i][1] is not "CD") and \
            (lemma[i] not in stops)):
            stn.append(Token(tokens[i], lemma[i], tagged_words[i][1]))
    return stn              

# Apply Lemmatization and regular expression constraints
def getLemma(tokens):
    lemma = []
    for token in tokens:
        term = token.lower()
        #lem_term = lemmatizer.lemmatize(term)
        # Regular expression constraint - do not allow [:;=+-,.\(\)\"\[\]'] at first position
        if (len(term) > 1 and (re.sub("[:;=+-,.\(\)\"\[\]']", "" , term[0]) != term[0]) and term[1] >= 'a' and term[1] <= 'z'):
            lemma.append(term[1:])
        else:
            lemma.append(term)
    return lemma  

# Save Final Aspect Annotated Sentences
def saveAnnotatedSentences(m_sentences_annotated, q_sentences,filename,survey_id,provider):
    joined_sentences = []
    sentences_id = []
    aspect_annot = []
    # print("test",survey_id,provider)
    for stn in m_sentences_annotated:
       
        sentences_id.append(stn.rid)
        aspect_annot.append(stn.aspectID)

        wtokens = []
        for tkn in stn.ttoken:
            wtokens.append(tkn.lemma)
        
        sentences=" ".join(wtokens)
        joined_sentences.append(" ".join(wtokens))
    # ChiFinal(survey_id=survey_id,provider=provider,data={"RID":sentences_id, "sentences":joined_sentences, "aspects":aspect_annot, "original":q_sentences})
    
    output = pd.DataFrame( data={"RID":sentences_id, "sentences":joined_sentences, "aspects":aspect_annot, "original":q_sentences})     
    output.to_csv("aspect/"+filename+"#"+survey_id+"#"+provider)    

# Save final Aspect Keywords list
def saveExtendedAspectKeywords(m_aspectkeywords_fixed,AOutfilename):    
    f = open(AOutfilename, 'w')
    for key, value in m_aspectkeywords_fixed.items():
        f.write(key + ': ')
        for v in value:
            f.write(v + ' ')
        f.write('\n')
    f.close()        
        
class ReviewP(object):
    def __init__(self,survey_id,provider):
        self.sid= survey_id
        self.p= provider
        # self.s= sector
    def run(self):
        m_aspectkeywords = aspectSegmenter.loadAspectKeywords('aspect/Data/restaurant_bootstrapping.dat')
        q_sentences = loadReviewAndProcess(self.sid)
        # print(q_sentences)
        m_sentences_annotated, m_aspectkeywords_fixed = aspectSegmenter.BootStrapping(m_sentences, m_vocabulary, m_aspectkeywords)
        saveAnnotatedSentences(m_sentences_annotated, q_sentences,"Data/annotated_sentences_chi_final.csv",self.sid,self.p)
        saveExtendedAspectKeywords(m_aspectkeywords_fixed,'aspect/Data/restaurant_bootstrapped_keywords_chi_final.dat')
        print("Review Processing Done!")

        
if __name__=='__main__':
    # os.chdir('..')
    # os.chdir('..')
    print ('Load Aspect Seed Words...')
    m_aspectkeywords = aspectSegmenter.loadAspectKeywords('Data/restaurant_bootstrapping.dat')
    print ('Load Reviews And Process...')
    q_sentences = loadReviewAndProcess('Data/reviews.csv')
    print ('Start Bootstrapping For Aspect Segmentation')
    m_sentences_annotated, m_aspectkeywords_fixed = aspectSegmenter.BootStrapping(m_sentences, m_vocabulary, m_aspectkeywords)
    print ('Saving Annotated sentences and extended aspect keywords list')
    saveAnnotatedSentences(m_sentences_annotated, q_sentences,'Data/annotated_sentences_chi_final.csv')
    print ('Saving Extended Aspect Keyword list')
    saveExtendedAspectKeywords(m_aspectkeywords_fixed,'Data/restaurant_bootstrapped_keywords_chi_final.dat')
    
# if nltk errors go refer this 
# http://stackoverflow.com/questions/4867197/failed-loading-english-pickle-with-nltk-data-load
# http://stackoverflow.com/questions/8590370/how-to-do-pos-tagging-using-the-nltk-pos-tagger-in-python
# Zurez
