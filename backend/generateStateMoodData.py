import tweepy
import re
from sklearn.externals import joblib
from numpy import loadtxt,transpose
import time

start_time = time.time()

def oAuth():
    print("authorising")
    # Twitter Oauth handshake
    OAuthkeys = loadtxt("config",dtype = str)
    OAuthkeys = dict(zip(OAuthkeys[:,0], OAuthkeys[:,1]))
    auth      = tweepy.OAuthHandler(OAuthkeys["consumerKey"], OAuthkeys["consumerSecret"])
    auth.set_access_token(OAuthkeys["accessToken"], OAuthkeys["accessTokenSecret"])
    api       = tweepy.API(auth)
    return(api)

# generate the model
print('generating model')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import pandas as pd


# 0 is sad, 1 is happy
#dat    = pd.read_csv('sentimentTrainingData/cleanedTweetSentimentAnalysisDataset.txt',sep=None,engine='python',usecols = [1,3]).values
dat    = pd.read_csv('sentimentTrainingData/xab',sep=None,engine='python',usecols = [1,3]).values
tweets = dat[:,1]
happy  = dat[:,0].astype(float)

count_vect        = CountVectorizer()
X_train_counts    = count_vect.fit_transform(tweets)
tfidf_transformer = TfidfTransformer()
X_train_tfidf     = tfidf_transformer.fit_transform(X_train_counts)
clf               = MultinomialNB().fit(X_train_tfidf, happy)


class stateTwitterMoodListener(tweepy.StreamListener):

    def __init__(self, states):
        self.states= states
        tweepy.StreamListener.__init__(self)


        # self.startListening()

    def startListening(self):
        self.stream = tweepy.Stream(auth = api.auth, listener=self)
        print(self.states)
        self.stream.filter(languages = ["en"],track=self.states.tolist(),async = True)

    def on_status(self, status):

        # get and process the tweet
        txt    = status.text
        txt    = re.sub('(RT )', '', txt)
        txt    = re.sub("(@[^\s]+)", '', txt)
        newDoc = [txt]

        for state in self.states:
            if state in (status.text or status.expanded_url or status.screen_name):
                # vectorize and extract tfidf
                X_new_counts = count_vect.transform(newDoc)
                X_new_tfidf  = tfidf_transformer.transform(X_new_counts)

                # predict tweet sentiment
                predicted  = clf.predict(X_new_tfidf)
                statesAndMoods[state][0] += (predicted[0]-.5)*2
                statesAndMoods[state][1] += 1
                updateData()

    def apoptos(self):
        self.stream.disconnect()



def updateData():
    f = open('../moodData/data.json','w')
    dt = (time.time() - start_time)
    f.write('{')
    for state in statesAndMoods:

        totalMood   = statesAndMoods[state][0]
        totalTweets = statesAndMoods[state][1]
        mood = str(float(totalMood)/totalTweets)
        x = statesAndMoods[state][2]
        y = statesAndMoods[state][3]
        # if state != statesAndMoods.keys()[-1]:
        #     f.write('{"'+state+'":['+mood+','+str(x)+','+str(y)+']},\n')
        # else:
        #     f.write('{"'+state+'":"'+str(float(totalMood)/totalTweets)+'"}\n')
        #     f.write(']')
        if state != statesAndMoods.keys()[-1]:
            f.write('"'+state+'":'+mood+',\n')
        else:
            f.write('"'+state+'":'+mood+'}\n')
            # f.write('}')
        

    
    f.close()

api = oAuth()

print("loading state data")
statesAndCenters   = loadtxt("stateData/stateCenters.txt",dtype = str,delimiter  = ":",usecols  = (0,2))
states             = statesAndCenters[:,0]
centers = []
for i,center in enumerate(statesAndCenters[:,1]):
    coords = center.split(' ')
    coords[0] = float(coords[0])
    coords[1] = float(coords[1])
    centers.append(coords)
import numpy as np
centers = np.array(centers)
statesAndMoods = dict(zip(states, transpose([[0] * len(states),[1] * len(states),centers[:,0],centers[:,1]] ) ))

print("initializing listener")
listener = stateTwitterMoodListener(states)
listener.startListening()

print("initialized")
testVar = raw_input("t for terminate")
if testVar == 't':
     listener.apoptos()
