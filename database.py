import sqlite3

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
			Timestamp DATETIME NOT NULL,
			Hashtags INTEGER NOT NULL DEFAULT 0,
			Mentions INTEGER NOT NULL DEFAULT 0,
			Emojis INTEGER NOT NULL DEFAULT 0,
			Links INTEGER NOT NULL DEFAULT 0,
			ContainsMedia BOOLEAN NOT NULL DEFAULT 0,
			Sentiment TEXT,
			Subjectivity REAL,
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

def create_user(username, tweets, retweets, followers, friends, favourites,
				accountcreated, verified):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

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
	
def create_tweet(userid, twit_id, content, likes, retweets, timestamp, hashtags, mentions, emojis,
				 links, containsmedia):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()
	c.execute('''INSERT INTO Tweet (UserId, TwitterId, Content, Likes, Retweets, Timestamp, Hashtags, 
				Mentions, Emojis, Links, ContainsMedia)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
				[userid, twit_id, content, likes, retweets, timestamp, hashtags, mentions, emojis, links, containsmedia])

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

def update_user_retweets(user_id, retweet_count):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute("UPDATE User SET Retweets = ? WHERE Id = ?", [retweet_count, user_id])
	conn.commit()
	conn.close()
	
	
def update_tweet_sentiment(tweetid, sentiment, subjectivity):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	
	c.execute("UPDATE Tweet SET Sentiment = ?, Subjectivity = ? WHERE Id = ?", [sentiment, subjectivity, tweetid])
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

#Average tweets per day of user
def average_tweets_per_day(userid):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute('''SELECT AVG(TweetsOnDay) AS AvgTweetsPerDay
					FROM
					(
						SELECT UserId, DATE(Timestamp) AS Day, COUNT(*) AS TweetsOnDay
						FROM Tweet
						GROUP BY UserId, Day
					)
					WHERE UserId = ?
					GROUP BY UserId''', [userid])
				
	average_tweets = c.fetchone()
	conn.close()
	return average_tweets

#Average score of user tweets
def average_tweet_score(userid):
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute('''SELECT UserId, ROUND(AVG(score), 0) AS "AverageTweetScore"
				FROM Tweet
				WHERE UserId = ?
				GROUP BY UserId''', [userid])
				
	average_tweet_score = c.fetchone()
	conn.close()
	return average_tweet_score

#Get average likes for all positive tweets
def get_average_likes_for_positive_tweets():
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute('''SELECT ROUND(AVG(Likes),0) AS "AverageLikes"
				 FROM Tweet 
				 WHERE Sentiment = "pos" ''')
 
	average_likes = c.fetchone()
	conn.close()
	return average_likes


#Get average retweets for positive tweets
def get_average_retweets_for_positive_tweets():
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute('''SELECT ROUND(AVG(Retweets),0) AS "AverageRetweets"
				 FROM Tweet 
				 WHERE Sentiment = "pos" ''')
 
	average_retweets = c.fetchone()
	conn.close()
	return average_retweets


#Get average length of positive tweet content
def get_average_length_of_positive_tweets():
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	c.execute('''SELECT ROUND(AVG(length(content)),0) AS "AverageLength"
				 FROM Tweet 
				 WHERE Sentiment = "pos" ''')
 
	average_length = c.fetchone()
	conn.close()
	return average_length
	

#Drop database tables
def drop_database():
	conn = sqlite3.connect(dbname)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	
	c.execute("DROP TABLE IF EXISTS User")
	c.execute("DROP TABLE IF EXISTS Tweet")
	conn.commit()
	conn.close()


