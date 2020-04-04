import sqlite3

#CREATE TABLES
#ENSURE TABLES CREATED 
#INSERT USER VALUES
#INSERT TWEET VALUES
#GET ALL TWEETS
#GET ALL USERS
#UPDATE TWEET SENTIMENT
#UPDATE TWEET SCORE
#UPDATE USER SCORE
#UPDATE USER TOTALSCORE



dbname = "twitterDatabase.db"   



def initialise():
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	c.execute("PRAGMA foreign_keys = ON")
	c.execute('''
		CREATE TABLE IF NOT EXISTS User (
			Id INTEGER PRIMARY KEY AUTOINCREMENT,
			Username TEXT NOT NULL UNIQUE,
			Tweets INTEGER NOT NULL DEFAULT 0,
			Retweets INTEGER NOT NULL DEFAULT 0,
			Followers INTEGER NOT NULL DEFAULT 0,
			Friends INTEGER NOT NULL DEFAULT 0, 
			Favourites INTEGER NOT NULL DEFAULT 0,
			AccountCreated DATETIME NOT NULL, 
			Verified BOOLEAN NOT NULL DEFAULT 0,
			Score REAL, 
			TotalScore REAL
		)	
	''')
	
	c.execute('''
		CREATE TABLE IF NOT EXISTS Tweet ( 
			Id INTEGER PRIMARY KEY AUTOINCREMENT,
			TwitterId INTEGER NOT NULL,
			UserId INTEGER NOT NULL, 
			Content TEXT NOT NULL,
			Likes INTEGER NOT NULL DEFAULT 0,
			Retweets INTEGER NOT NULL DEFAULT 0,
			Replies INTEGER NOT NULL DEFAULT 0, 
			Timestamp DATETIME NOT NULL,
			Hashtags INTEGER NOT NULL DEFAULT 0,
			Mentions INTEGER NOT NULL DEFAULT 0,
			Emojis INTEGER NOT NULL DEFAULT 0,
			Links INTEGER NOT NULL DEFAULT 0,
			ContainsMedia BOOLEAN NOT NULL DEFAULT 0,
			Sentiment TEXT,
			Score REAL,
			FOREIGN KEY (UserId) 
				REFERENCES User (Id)
		)
	''')
	conn.commit()
	conn.close()
	
def check_tables_exist():
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	c.execute(''' 
		SELECT COUNT(*) 
		FROM sqlite_master 
		WHERE type='table' 
		AND name='User'
	''')
	user_table_result = c.fetchone()
	
	c.execute(''' 
		SELECT COUNT(*)
		FROM sqlite_master
		WHERE type='table'
		AND name='Tweet'
	''')
	tweet_table_result = c.fetchone()
	conn.close()

	user_table_exists = user_table_result[0] == 1
	tweet_table_exists = tweet_table_result[0] == 1
	return tweet_table_exists and user_table_exists

def user_exists(username):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	c.execute(''' 
		SELECT COUNT(*) 
		FROM User 
		WHERE Username=?
	''', [username])
	user_result = c.fetchone()
	conn.close()

	user_exists = user_result[0] == 1
	return user_exists

def tweet_exists(twit_id):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	c.execute(''' 
		SELECT COUNT(*) 
		FROM Tweet 
		WHERE TwitterId=?
	''', [twit_id])
	tweet_result = c.fetchone()
	conn.close()

	tweet_exists = tweet_result[0] == 1
	return tweet_exists

def create_or_update_user(username, tweets, retweets, followers, friends, favourites,
				accountcreated, verified):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	exists = user_exists(username)

	if exists:
		c.execute('''UPDATE User
			SET Tweets = ?, Retweets = ?, Followers = ?, Friends = ?, Favourites = ?, AccountCreated = ?, Verified = ?
			WHERE Username = ?''',
			[tweets, retweets, followers, friends, favourites, accountcreated, verified, username])
	else:
		c.execute( '''INSERT INTO User (Username, Tweets, Retweets, Followers, Friends, Favourites, AccountCreated, Verified)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
			[username, tweets, retweets, followers, friends, favourites, accountcreated, verified])

	conn.commit()

	c.execute(''' 
		SELECT Id 
		FROM User 
		WHERE Username=?
	''', [username])
	user_id = c.fetchone()[0]

	conn.close()
	return user_id	
	
def create_or_update_tweet(userid, twit_id, content, likes, retweets, replies, timestamp, hashtags, mentions, emojis,
				 links, containsmedia):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	exists = tweet_exists(twit_id)

	if exists:
		c.execute('''UPDATE Tweet
			SET UserId = ?, Content = ?, Likes = ?, Retweets = ?, Replies = ?, Timestamp = ?, Hashtags = ?, 
			Mentions = ?, Emojis = ?, Links = ?, ContainsMedia = ?''',
			[userid, content, likes, retweets, replies, timestamp, hashtags, mentions, emojis, links, containsmedia])
	else:
		c.execute('''INSERT INTO Tweet (UserId, TwitterId, Content, Likes, Retweets, Replies, Timestamp, Hashtags, 
			Mentions, Emojis, Links, ContainsMedia)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
			[userid, twit_id, content, likes, retweets, replies, timestamp, hashtags, mentions, emojis, links, containsmedia])

	conn.commit()
	conn.close()

def get_all_tweets():
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute("SELECT * FROM Tweet")
	tweets = c.fetchall()
	conn.close()
	return tweets
	
def get_all_users():
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute("SELECT * FROM User")
	users = c.fetchall()
	conn.close()
	return users
	
def update_tweet_sentiment(tweetid, sentiment):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	
	c.execute("UPDATE Tweet SET Sentiment = ? WHERE Id = ?", [sentiment, tweetid])
	conn.commit()
	conn.close()

def update_tweet_score(tweetid, score):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute("UPDATE Tweet SET Score = ? WHERE Id = ?", [score, tweetid])
	conn.commit()
	conn.close()
	
def update_user_score(userid, score):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	
	c.execute("UPDATE User SET Score = ? WHERE Id = ?", [score, userid])
	conn.commit()
	conn.close()
	
def update_user_total_score(userid, totalscore):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	
	c.execute("UPDATE User SET TotalScore = ? WHERE Id = ?", [totalscore, userid])
	conn.commit()
	conn.close()

def drop_database():
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	
	c.execute("DROP TABLE IF EXISTS User")
	c.execute("DROP TABLE IF EXISTS Tweet")
	conn.commit()
	conn.close()


drop_database()	
#initialise()
# print(check_tables_exist())
#create_or_update_user("vitamin_d", 69, 12, 420, 1, 20, "2019-04-02", True)
#create_or_update_user("vitamin_d", 19581, 1231, 541452, 45245, 452452, "2019-12-11", False)

# print(get_all_users())
# create_tweet(1, "here is a tweet", 20, 2, 5, "2020-03-26:11:51:30", 2,
# 			 0, 2, 1, False)
# print(get_all_tweets())
# #TWITTER DATETIME DISPLAYS AS: "THU MAR 26 11:51:30 +0000 2020"

# update_tweet_sentiment(1, "Positive")
# print(get_all_tweets()[0]["sentiment"])

# update_tweet_score(1, 20.50)
# print(get_all_tweets()[0]["score"])

# update_user_score(1, 50.20)
# print(get_all_users()[0]["score"])

# update_user_total_score(1, 100.00)
# print(get_all_users()[0]["totalscore"])

