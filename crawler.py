import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import numpy as np
import pandas as pd
import database


##TO DO:##
##ACCESS ALL RELEVANT INFORMATION##
##POPULATE DATABASE WITH TWITTER INFO##
##APPLY NLP TO DATABASE##
##GENERATE USER SCORE BASED ON CHARACTERISTICS##
##GENERATE FINAL SCORE##
##WEEP UNCONTROLLABLY##


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

class TweetAnalyser():

	#Functionality for analysing and categorizing content from tweets
	
	def tweets_to_data_frame(self, tweets):
		df = pd.DataFrame(data=[tweet.id for tweet in tweets], columns =['id'])

		for tweet in tweets:
			df['content'] = np.array([tweet.text for tweet in tweets])
			df['date'] = np.array([tweet.created_at for tweet in tweets])
			df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
			df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
			#df['hashtags'] = np.array([tweet.entities["hashtags"][0] for tweet in tweets])
			#df['links'] = np.array([tweet.entities.urls for tweet in tweets])
			#df['mentions'] = np.array([tweet.entities.user_mentions for tweet in tweets])
			#df['contains_media'] = np.array([tweet.entities.media for tweet in tweets])
			#print(tweet.entities.keys())
		
		return df

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

if 	__name__ == "__main__":
	
	database.initialise()
	twitter_client = TwitterClient()
	tweet_analyser = TweetAnalyser()
	users = ['realDonaldTrump']
	
	
	api = twitter_client.get_twitter_client_api()
	all_tweets = pd.DataFrame([])
	
	for user in users:
		tweets = get_tweets_for_user(user)
		for tweet in tweets:
			content = tweet.text
			date = tweet.created_at
			likes = tweet.favorite_count
			retweets = tweet.retweet_count
			print("content = %s date = %s likes = %s retweets = %s"%(content,date,likes,retweets))
			
			


		# tweets = api.user_timeline(screen_name=user, count=10)
		# df = tweet_analyser.tweets_to_data_frame(tweets)
		# pd.set_option('display.max_colwidth',-1)
		# #print(df.head(10))
		# all_tweets = all_tweets.append(df)
		
	##PRINT HASHTAGS IF HASHTAGS > 0##	
	# for tweet in tweets:
	# 		detail = api.get_status(tweet.id)
	# 		if len(detail.entities["hashtags"]) > 0:
	# 				print(detail.entities["hashtags"][0]["text"])

	##PRINT URL IF URLS >0##
	# for tweet in tweets:
	# 	detail = api.get_status(tweet.id)
	# 	if len(detail.entities["urls"]) > 0:
	# 		print(detail.entities["urls"][0])

	##PRINT USER_MENTIONS IF MENTIONS > 0##
	# for tweet in tweets:
	# 	detail = api.get_status(tweet.id)
	# 	if len(detail.entities["user_mentions"]) > 0:
	# 		print(detail.entities["user_mentions"][0])

	# for tweet in tweets:
	# 	detail = api.get_status(tweet.id)
	# 	if len(detail.entities["media"]) > 0:
	# 		print(detail.entities["media"][0])
	
	#shows what can be extracted from tweets#
	#print(dir(tweets[0]))
	#print(tweets[0].retweet_count)
	
	#print(dir(tweets[0])) 
	#print(all_tweets.to_json(orient='records'))
	all_tweets_json = all_tweets.to_json(orient='records')
	
	with open('tweetsTest.json','a') as outfile:
		outfile.write(all_tweets_json)
		outfile.close


		##Getting tweet from user##
		# twitter_client = TwitterClient('Vitamin_D91')
		# my_tweets = (twitter_client.get_user_timeline_tweets(3200))
		# for i in range(len(my_tweets)):
		# 		print(i + 1, my_tweets[i])


			

		#examples for using classes 
		
		#hash_tag_list = ["donald trump"]
		#fetched_tweet_filename = "tweets.json"
		
		#Specified user and number of tweets from Cursor
		#twitter_client = TwitterClient('realDonaldTrump')
		#print(twitter_client.get_user_timeline_tweets(1))
		
		#twitter_streamer = TwitterStreamer()
		#twitter_streamer.stream_tweets(fetched_tweet_filename, hash_tag_list)

	
	
	