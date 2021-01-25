# Honours-Project

This is my fourth year honours project: Using Natural Language Processing and User Features to Detect and Rank Twitter Accounts.

The aim of this project was to create an app which would generate a score for a Twitter user based on a number of factors in order to
determine whether the account was likely to be malicious or trustworthy in terms of the rhetoric that it used. This project is made up
of 5 seperate components: 

# Twitter Crawler
To capture the data used in the further elements of the project, I created a Twitter crawler which
allowed for information regarding both the tweet itself and the user who posted it to be gathered. 

The crawler utilises the Tweepy API, an open-source python librabry, in order to interact with Twitter as their own API is incredibly restrictive.
It takes a username (user.screen_name) and returns the metadata for each tweet. Using this, it is possible to extract further data, such as 
determining the amount of tweets made per day based on the times they were posted. 

# Database
An SQLite 3 database is employed in order to store and manipulate the data gained from the crawler. This allows for methods to be written in 
order to gain further information on the metadata and serves as the source of information for the Natural Language Processing.

![alt text](https://github.com/VitaminD91/Honours-Project/blob/master/DatabaseQ's.jpg?raw=true)

# Natural Language Processing
In order to process the text being added to the database, I used TextBlob, a python library used for processing textual data. The TextBlob API
allowed for sentiment analysis & classification. A combination of the text from each tweet and the details of user were combined in order to 
generate a score based on the results. 

# Scoring Algorithm
Scores were generated based on certain elements of both an account, and the tweets that an account has made. This score was then combined, 
with each given a certain weight toward the final total score. Factors that effected this were such things as: The amount of time an account
has been active, the number of followers for an account and the number of accounts they were following, whether tweets contained media or not, 
and various other factors which are outlined within the dissertation. These factors were decided based on what seemed to be the most common 
similarities in all malicious accounts based on various studies. 

![alt text](https://github.com/VitaminD91/Honours-Project/blob/master/SystemArchitectureDiagram.jpg?raw=true)

