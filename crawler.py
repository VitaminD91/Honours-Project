import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import math
import numpy as np
import pandas as pd
import database
from emoji import UNICODE_EMOJI
from tweetIds import tweet_ids


##TO DO:##
##GENERATE USER SCORE BASED ON CHARACTERISTICS##
##GENERATE FINAL SCORE##




#list of twitter application keys
consumer_key = "meHA7BPQcpjjQI5PAYMPJSVcG"
consumer_secret = "jmOCuYgCzAGOgzElaXWME8CAlyhl1ePIwQEvOZs1O067nIFm7H"
access_token = "1183756062710751232-9mT3KIzwJfn3upsioWEl9Lmg3xvRYu"
access_token_secret = "Zz6252rtCLx5vJBu1Tp7MBnvepvDu1G0XLcYJ9ektsuxS"


# # # # # TWITTER CLIENT # # # # #

class TwitterClient():
	def __init__(self, twitter_user=None):
		self.auth = TwitterAuthenticator().authenticate_twitter_app()
		self.twitter_client = API(self.auth)
		
		self.twitter_user = twitter_user
		
	def get_twitter_client_api(self):
		return self.twitter_client
	
	#returns a specified number of tweets from given user (defaults to self if no specified user)	
	def get_user_timeline_tweets(self, num_tweets):
		tweets = []
		for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
			tweets.append(tweet)
		return tweets
	
	#returns specified number of friends from friend list from a given user (defaults to self)
	def get_friend_list(self, num_friends):
		friend_list = []
		for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
			friend_list.append(friend)
		return friend_list
	
	#returns specified number of tweets from given user's home timeline (defaults to self)	
	def get_home_timeline_tweets(self, num_tweets):
		home_timeline_tweets = []
		for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
			home_timeline_tweets.append(tweet)
		return home_timeline_tweets

# # # # # TWITTER AUTHENTICATOR # # # # # 		



class TwitterAuthenticator():
	
	def authenticate_twitter_app(self):
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		return auth

		
# # # # # TWITTER STREAMER # # # # #
		
class TwitterStreamer():
	
	def	__init__(self):
		self.twitter_authenticator = TwitterAuthenticator()
		
	def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
		"""This handles twitter authentication and the connection to the twitter
		streaming API"""
		listener = TwitterListener(fetched_tweet_filename)
		auth = self.twitter_authenticator.authenticate_twitter_app()
		stream = Stream(auth, listener)
		stream.filter(track=hash_tag_list)
	

# # # # # TWITTER LISTENER # # # # #
	
class TwitterListener(StreamListener):
	"""This is a basic listener class that just prints recived tweets to stdout"""
	
	def __init__ (self, fetched_tweet_filename=None):
		if fetched_tweet_filename is None:
			fetched_tweet_filename = "file.txt"
		self.fetched_tweet_filename = fetched_tweet_filename

	def on_data(self, data):
		tweet_data = json.dumps(data, indent=4)
		try:
			print(tweet_data)
			with open(self.fetched_tweet_filename, 'a') as tf:
				tf.write(tweet_data)
			return True
		except BaseException as e:
			print("Error on data: %s" % str(e))
		return True 
	
	def on_error(self, status):
		if status == 420:
			#Returns False in case of rate limit
			return False
		print(status)
		
		
# # # # #	TWEET ANALYSER # # # # #

twitter_client = TwitterClient()
api = twitter_client.get_twitter_client_api()


def get_tweets_for_user(username):
	alltweets = []
	new_tweets = api.user_timeline(screen_name=username, count=200)    
	alltweets.extend(new_tweets)    
	oldest = alltweets[-1].id - 1
	
	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name=username, count=200, max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1
	
	return alltweets

def get_user_details(username):
	user = api.get_user(username)
	return user

def is_emoji(s):
	count = 0
	for emoji in UNICODE_EMOJI:
		count += s.count(emoji)
		if count > 1:
			return False	
	return bool(count)


def get_author_from_tweet_id(id_list):
	tweets = api.statuses_lookup(id_list)
	usernames = []
	for tweet in tweets:
		usernames.append(tweet.user.screen_name)
	return usernames


def fetch_usernames(array):
	batch_size = 100
	array_size = len(array)
	batch_count = math.ceil(array_size / batch_size)

	usernames = []
	for i in range(0, batch_count):
		start_ix = i * batch_size
		end_ix = start_ix + batch_size
		batch = array[start_ix:end_ix]
		print(len(batch))
		if len(batch) > 0:
			usernames.extend(get_author_from_tweet_id(batch))
	usernames = list(dict.fromkeys(usernames))
	return usernames


if 	__name__ == "__main__":
	
	database.drop_database()
	database.initialise()

	users = fetch_usernames(tweet_ids)
	
	all_tweets = pd.DataFrame([])
	
	for user in users:
		user_details = get_user_details(user)
		followers = user_details.followers_count
		friends = user_details.friends_count
		favourites = user_details.favourites_count
		account_created = user_details.created_at
		verified = user_details.verified

		tweets = get_tweets_for_user(user)
		tweet_count = len(tweets)

		#persist
		print("Creating user: " + str(user))
		user_id = database.create_user(user, tweet_count, 0, followers, friends, favourites, account_created, verified)

		retweet_count = 0
		print("Creating Tweets...")
		for tweet in tweets:			
			content = tweet.text
			if (str.startswith(content, "RT")):
				retweet_count = retweet_count + 1
			else:
				twit_id = tweet.id
				likes = tweet.favorite_count
				retweets = tweet.retweet_count
				timestamp = tweet.created_at
				hashtag_count = len(tweet.entities["hashtags"])
				mention_count = len(tweet.entities["user_mentions"])
				emoji_count = 0
				for char in content:
					if is_emoji(char):
						emoji_count += 1
				link_count = len(tweet.entities["urls"])
				contains_media = "media" in tweet.entities
				database.create_tweet(user_id, twit_id, content, likes, retweets, timestamp, hashtag_count, mention_count, emoji_count, link_count, contains_media)



		#persist again but with retweets
		database.update_user_retweets(user_id, retweet_count)
		

	all_tweets_json = all_tweets.to_json(orient='records')
	
	with open('tweetsTest.json','a') as outfile:
		outfile.write(all_tweets_json)
		outfile.close


