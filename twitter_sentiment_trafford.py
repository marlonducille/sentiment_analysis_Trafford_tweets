
#https://datascienceplus.com/brexit-tweets-sentiment-analysis-in-python/

import tweepy
import codecs
from aylienapiclient import textapi
import io
import csv

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '449899233-9UUXIXAkVl40IhE6JURBLatyCOnzqCHW9GZ8fziD'
ACCESS_SECRET = 'NVkN56qyYBLwHNLDWdKuJA7ewvftq4xOKZwCyjMtSTNJP'
CONSUMER_KEY = 'hS3ks8CVC0cYpVsLFyssqRNO1'
CONSUMER_SECRET = 'xeJlHWP3mDLkTzTXsGEeVOfV28DUmAyW1MVUJ0Yw0CZQKN582X'

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= Ture;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#---------------------------------------------------------------------------------------------------------------------


search_results = api.search(q = "#Trafford", lang = "en", result_type = "recent", count = 100, until = '2019-04-26')      

# creating the corpus file                            
file = codecs.open("tweet_about_trafford.txt", "w", "utf-8")
for result in search_results:
    file.write(result.text)
    file.write("\n")
file.close()    

# determine which tweet is positive, negative or neutral          

# Initialize a new client of AYLIEN Text API
client = textapi.Client("xxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxx") #https://aylien.com/




with io.open('tweet_about_trafford.csv', 'w', encoding='utf8', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Tweet", "Sentiment"])
    with io.open("tweet_about_trafford.txt", 'r', encoding='utf8') as f:
        for trafford_tweet in f.readlines():
            ## Remove extra spaces or newlines around the text
            tweet = trafford_tweet.strip()
            ## Reject tweets which are empty so you don’t waste your API credits
            if len(tweet) < 10:
               # print('skipped')
                continue
            ## Make call to AYLIEN Text API
            sentiment = client.Sentiment({'text': tweet})

            ## Write the sentiment result into csv file
            csv_writer.writerow([sentiment['text'], sentiment['polarity']])              