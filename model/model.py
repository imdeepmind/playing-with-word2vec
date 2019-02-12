import pandas as pd
import re
import gensim
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

data = pd.read_csv('tweets.csv')

text = data['text'].values

del data

tweets = []

def clean_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', tweet)
    tweet = re.sub(r'\b[0-9]+\b\s*', '', tweet)
    if tweet[0:2] == 'rt':
        tweet = tweet.replace("rt  ", "")
    return tweet

for tweet in text:
    tweet = clean_tweet(tweet)
    words = word_tokenize(tweet)
    
    tweet = [t for t in tweet if t.isalpha()]
    stop_words = set(stopwords.words('english'))
    tweet = [t for t in words if not t in stop_words]
    
    tweets.append(tweet)

del text

num = {}

for tweet in tweets:
    for word in tweet:
        if word in num:
            num[word] += 1
        else:
            num[word] = 1

threshold = 20

cleaned_tweets = []

for tweet in tweets:
    temp = []
    for word in tweet:
        if num[word] >= threshold:
            temp.append(word)
    cleaned_tweets.append(temp)

model = gensim.models.Word2Vec(sentences=cleaned_tweets, size=100, window=5, workers=4, min_count=1)

model.wv.save_word2vec_format('model.bin', binary=True)