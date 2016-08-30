from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import pandas as pd



def generateSentimentAnalyser(data,catagory):
    count_vect        = CountVectorizer()
    X_train_counts    = count_vect.fit_transform(data)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf     = tfidf_transformer.fit_transform(X_train_counts)
    clf               = MultinomialNB().fit(X_train_tfidf, catagory)

    
    joblib.dump(tfidf_transformer, 'pkldModelComponents/tfidf_transformer.pkl') 
    joblib.dump(count_vect, 'pkldModelComponents/countVectorizer.pkl') 
    joblib.dump(clf, 'pkldModelComponents/tweetSentimentClassifier.pkl')

    return(clf)


# 0 is sad, 1 is happy
dat    = pd.read_csv('sentimentTrainingData/cleanedTweetSentimentAnalysisDataset.txt',sep=None,engine='python',usecols = [1,3]).values
tweets = dat[:,1]
happy  = dat[:,0].astype(float)

generateSentimentAnalyser(tweets,happy)