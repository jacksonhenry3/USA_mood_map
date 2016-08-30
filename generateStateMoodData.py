import tweepy
import re
from sklearn.externals import joblib
from numpy import loadtxt,transpose
import time
start_time = time.time()




def oAuth():
    print "authorising"
    # Twitter Oauth handshake
    OAuthkeys = loadtxt("config",dtype = str)
    OAuthkeys = dict(zip(OAuthkeys[:,0], OAuthkeys[:,1]))
    auth      = tweepy.OAuthHandler(OAuthkeys["consumerKey"], OAuthkeys["consumerSecret"])
    auth.set_access_token(OAuthkeys["accessToken"], OAuthkeys["accessTokenSecret"])
    api       = tweepy.API(auth)
    return(api)


print "loading model components"
# load in the model components
clf               = joblib.load('pkldModelComponents/tweetSentimentClassifier.pkl') #classifier
count_vect        = joblib.load('pkldModelComponents/countVectorizer.pkl')          #tweet vetorizer
tfidf_transformer = joblib.load('pkldModelComponents/tfidf_transformer.pkl')        #tfidf calc



class stateTwitterMoodListener(tweepy.StreamListener):

    def __init__(self, states):
        self.states= states
        tweepy.StreamListener.__init__(self)


        # self.startListening()

    def startListening(self):
        self.stream = tweepy.Stream(auth = api.auth, listener=self)
        print self.states
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

    # def apoptos(self):
    #     self.stream.disconnect()



def updateData():
    f = open('moodData.txt','w')
    dt = (time.time() - start_time)
    print dt
    for state in statesAndMoods:
        totalMood   = statesAndMoods[state][0]
        totalTweets = statesAndMoods[state][1]
        tweetRate   = totalTweets/dt
        f.write(state+","+str(float(totalMood)/totalTweets)+'\n')
    f.close()

api = oAuth()

print "loading state data"
statesAndCenters   = loadtxt("stateData/stateCenters.txt",dtype = str,delimiter  = ":",usecols  = (0,2))
states             = statesAndCenters[:,0]
# centers            = statesAndCenters[:,1]
statesAndMoods = dict(zip(states, transpose([[0] * len(states),[1] * len(states)] ) ))
# print statesAndMoods

print "initializing listener"   
listener = stateTwitterMoodListener(states)
listener.startListening()

print "initialized"