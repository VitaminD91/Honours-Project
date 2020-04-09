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




def classify_tweets():
    tweets = database.get_all_tweets()
    for tweet in tweets:
        sentiment = calculate_tweet_classification(tweet["content"])
        subjectivity = calculate_tweet_subjectivity(tweet["content"]) 
        database.update_tweet_sentiment(tweet["id"], sentiment, subjectivity)

    

def calculate_tweet_classification(content):
    tweet_classification = cl.classify(content)
    return tweet_classification
    


# 0.0 = very objective 1.0 = very subjective 
def calculate_tweet_subjectivity(content):
    tweet_content = TextBlob(content)
    tweet_subjectivity = tweet_content.sentiment.subjectivity
    print(tweet_subjectivity)
    return tweet_subjectivity
    
cl = NaiveBayesClassifier(train)
classify_tweets()