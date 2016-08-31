from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import pandas as pd

print('loaded resource')

def generateSentimentAnalyser(data,catagory):
    count_vect        = CountVectorizer()
    X_train_counts    = count_vect.fit_transform(data)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf     = tfidf_transformer.fit_transform(X_train_counts)
    clf               = MultinomialNB().fit(X_train_tfidf, catagory)

    print('beginig dump')
    print('dumping tfidf transformer')
    joblib.dump(tfidf_transformer, 'pkldModelComponents/tfidf_transformer.pkl') 
    print('dumping coun t vectoorizer')
    joblib.dump(count_vect, 'pkldModelComponents/countVectorizer.pkl') 
    print('dumping classifier')
    joblib.dump(clf, 'pkldModelComponents/tweetSentimentClassifier.pkl')

    return(clf)

print('loading data')
# 0 is sad, 1 is happy
dat    = pd.read_csv('sentimentTrainingData/cleanedTweetSentimentAnalysisDataset.txt',sep=None,engine='python',usecols = [1,3]).values
print('tweets loaded')
tweets = dat[:,1]
happy  = dat[:,0].astype(float)

generateSentimentAnalyser(tweets,happy)
