from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import database

train = [
    ('I love this sandwich.', 'pos'),
    ('this is an amazing place!', 'pos'),
    ('I feel very good about these beers', 'pos'),
    ('this is my best work.', 'pos'),
    ('what an awesome view', 'pos'),
    ('I love refridgerators', 'pos'),
    ('I do not like restaurant', 'neg'),
    ('I am tired of this stuff', 'neg'),
    ("I can't deal with this", 'neg'),
    ('he is my sworn enemy!', 'neg'),
    ('my boss is horrible', 'neg'),
    ('I hate doing this', 'neg')
]
test = [
    ('the beer was good', 'pos'),
    ('I do not enjoy my job', 'neg'),
    ("I ain't feeling dandy today.", 'neg'),
    ('I feel amazing today!', 'pos'),
    ('Gary is a friend of mine', 'pos'),
    ("I can't believe I'm doing this.", 'neg')
]


cl = NaiveBayesClassifier(train)

print(cl.classify("this is an amazing library!"))
print(cl.classify("I really don't like this at all"))

print(cl.accuracy(test))


def calculate_tweet_classification(content)
    tweet_classification = content.classification

def calculate_tweet_sentiment(content):
    tweet_sentiment = content.sentiment

def calculate_tweet_polarity(conent):
    tweet_polarity = content.polarity
    
