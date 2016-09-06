from json import dump
from re import sub
import tweepy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from pandas import read_csv


def oAuth():
    print("authorising")
    # Twitter Oauth handshake
    OAuthkeys = read_csv("config", skiprows=None).values
    OAuthkeys = {arr[0]: arr[1] for arr in OAuthkeys}
    auth = tweepy.OAuthHandler(OAuthkeys["consumerKey"],
                               OAuthkeys["consumerSecret"])
    auth.set_access_token(OAuthkeys["accessToken"],
                          OAuthkeys["accessTokenSecret"])
    api = tweepy.API(auth)
    return(api)

# generate the model
print ("loading data")

# 0 is sad, 1 is happy
# dat    = pd.read_csv('sentimentTrainingData/cleanedTweetSentimentAnalysisDataset.txt',sep=None,engine='python',usecols = [1,3]).values
dat = read_csv('sentimentTrainingData/cleanedTweetSentimentAnalysisDataset.txt'
               , sep=None, engine='python', usecols=[1, 3]).values
tweets = dat[:, 1]
happy = dat[:, 0].astype(float)

print('generating model')

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(tweets)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, happy)

class stateTwitterMoodListener(tweepy.StreamListener):
    """ Class which extends tweepy stream listener """

    def __init__(self, states):
        self.states= states
        tweepy.StreamListener.__init__(self)

    def startListening(self):
        self.stream = tweepy.Stream(auth=api.auth, listener=self)
        self.stream.filter(languages=["en"],
                           locations=[-124.8,25.01,-66.97,49.21],async = True)

    def on_status(self, status):

        # get and process the tweet
        txt = status.text
        txt = sub('(RT )', '', txt)
        txt = sub("(@[^\s]+)", '', txt)
        txt = [txt]

        for i in range(len(self.states)):
            if (self.states[i][0] or self.states[i][1]) in (status.place.full_name):
                state = self.states[i][1]
                # vectorize and extract tfidf
                X_new_counts = count_vect.transform(txt)
                X_new_tfidf  = tfidf_transformer.transform(X_new_counts)

                # predict tweet sentiment
                predicted  = clf.predict(X_new_tfidf)
                stateTweets[state]["tweets"].append({"text":txt[0],"mood":(predicted[0]-.5)*2.})
                if stateTweets[state]["totalTweets"]>=100:
                    stateTweets[state]["tweets"].pop(0)
                    print 'to many tweets about '+state
                updateData()
                break

    def apoptos(self):
        self.stream.disconnect()



def updateData():

    # calculate meta data about all the states tweets
    for state in stateTweets:
        stateTweets[state]["totalTweets"] = len(stateTweets[state]["tweets"])
        stateTweets[state]["totalMood"] = sum([tweet["mood"] for tweet in stateTweets[state]["tweets"]])
        stateTweets[state]["averageMood"] = stateTweets[state]["totalMood"] / max(1,stateTweets[state]["totalTweets"])

    with open("../moodData/data.json", "w") as statTwitterDataFile:
        dump(stateTweets, statTwitterDataFile, indent=4, sort_keys=True) #dumps data as json


api = oAuth()

states = [["HI", "Hawaii"], ["AK", "Alaska"], ["FL", "Florida"],
          ["NH", "New Hampshire"], ["MI", "Michigan"], ["VT", "Vermont"],
          ["ME", "Maine"], ["RI", "Rhode Island"], ["NY", "New York"],
          ["PA", "Pennsylvania"], ["NJ", "New Jersey"], ["DE", "Delaware"],
          ["MD", "Maryland"], ["VA", "Virginia"], ["WV", "West Virginia"],
          ["OH", "Ohio"], ["IN", "Indiana"], ["IL", "Illinois"],
          ["CT", "Connecticut"], ["WI", "Wisconsin"], ["NC", "North Carolina"],
          ["DC", "Washington"], ["MA", "Massachusetts"], ["TN", "Tennessee"],
          ["AR", "Arkansas"], ["MO", "Missouri"], ["GA", "Georgia"],
          ["SC", "South Carolina"], ["KY", "Kentucky"], ["AL", "Alabama"],
          ["LA", "Louisiana"], ["MS", "Mississippi"], ["IA", "Iowa"],
          ["MN", "Minnesota"], ["OK", "Oklahoma"], ["TX", "Texas"],
          ["NM", "New Mexico"], ["KS", "Kansas"], ["NE", "Nebraska"],
          ["SD", "South Dakota"], ["ND", "North Dakota"], ["WY", "Wyoming"],
          ["MT", "Montana"], ["CO", "Colarado"], ["ID", "Idaho"],
          ["UT", "Utah"], ["AZ", "Arizona"], ["NV", "Nevada"], ["OR", "Oregon"],
          ["WA", "Washington"], ["CA", "California"]]

stateTweets = {state[1]: {'tweets': [], 'totalTweets': .01, 'totalMood': 0,
               'averageMood': 0} for state in states}

print("initializing listener")
listener = stateTwitterMoodListener(states)
listener.startListening()

print("initialized")
testVar = raw_input("t for terminate")
if testVar == 't':
    listener.apoptos()
