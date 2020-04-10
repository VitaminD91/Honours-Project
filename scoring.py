import database
from datetime import datetime

#Calculate the score of a user
def calculate_user_score():
    
    users = database.get_all_users()

    for user in users:
        user_score = 100
        

        #friends less than followers
        if user["friends"] < user["followers"]:
            user_score -= 10
        
        #Account less than 50 days old
        dt = user["accountcreated"]
        parsed = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        now = datetime.today()
        diff = now - parsed

        #age of account
        if diff.days < 50: 
            user_score -=14 #based on the findings of research

        #average user tweets per day 
        avg_result = database.average_tweets_per_day(user["id"])
        tweets_per_day = avg_result["AvgTweetsPerDay"]
        if tweets_per_day > 20:
            user_score -= 30

        #verified status
        if user["verified"] == 1:
            user_score += 50

        #if user_score exceeeds 100, set score to 100 
        if user_score > 100:
            user_score = 100
        
        database.update_user_score(user["id"], user_score)

        return user_score

#Calculate the score for each tweet a user has made
def calculate_tweet_score():

    tweets = database.get_all_tweets()

    #get average likes for use
    average_result = database.get_average_likes_for_positive_tweets()
    average_likes = average_result["AverageLikes"]

    #get average retweets for use
    average_rt_result = database.get_average_retweets_for_positive_tweets()
    average_retweets = average_rt_result["AverageRetweets"]

    #get average length for use
    average_positive_length = database.get_average_length_of_positive_tweets()
    average_length = average_positive_length["AverageLength"]


    for tweet in tweets:
        tweet_score = 100

        #number of favourites > average
        if tweet["likes"] > average_likes:
            tweet_score -= 10

        #number of retweets > average
        if tweet["retweets"] > average_retweets: 
            tweet_score -= 10

        #contains URLS
        if tweet["links"] == 1:
            tweet_score -= 10

        #contains Hashtags
        if tweet["hashtags"] >= 2:
            tweet_score -= 20
        
        #contains emojis
        if tweet["emojis"] >= 2:
            tweet_score -= 10

        #contains media 
        if tweet["containsmedia"] == 1:
            tweet_score -= 10
        
        #contains mentions
        if tweet["mentions"] >= 2:
            tweet_score -= 20
        
        #sentiment is negative
        if tweet["sentiment"] == 'neg':
            tweet_score -= 30

        #subjectivity is bias
        if tweet["subjectivity"] < 0.5:
            tweet_score -= 10 

        #length of tweet less than average
        if tweet[len("content")] <= average_length:
            tweet_score -= 20

        database.update_tweet_score(tweet["Id"], tweet_score)


#Calculates the final score for a user                
def calculate_total_score():
    
    users = database.get_all_users()

    for user in users:
            
        score_result = database.average_tweet_score(user["id"])
        average_tweet_score = score_result["AverageTweetScore"]

        total_score = (user["score"] + average_tweet_score) / 2
        database.update_user_total_score(user["id"], total_score)



calculate_user_score()
calculate_tweet_score()
calculate_total_score()
print("Scoring Complete")