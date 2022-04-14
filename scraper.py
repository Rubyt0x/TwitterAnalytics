from colorama import Cursor
from twitter_keys import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

def get_twitter_client():
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client

def get_tweets_from_user(twitter_username, page_limit = 16, count_tweet = 200):
    client = get_twitter_client()
    all_tweets = []

    for page in tweepy.Cursor(client.user_timeline, screen_name = twitter_username, count = count_tweet).pages(page_limit):
        for tweet in page:
            parsed_tweet = {}
            parsed_tweet['date'] = tweet.created_at
            parsed_tweet['author'] = tweet.user.name
            parsed_tweet['twitter_name'] = tweet.user.screen_name
            parsed_tweet['text'] = tweet.text
            parsed_tweet['like_count'] = tweet.favorite_count
            parsed_tweet['retweet_count'] = tweet.retweet_count

            all_tweets.append(parsed_tweet)
    
    df = pd.DataFrame(all_tweets)
    df = df.drop_duplicates("text", keep = 'first')

    return df
            
Fuel = get_tweets_from_user("fuellabs_")

print("Data Shape: {}".format(Fuel.shape))

Fuel.to_csv('Fuel_tweets.csv', encoding='UTF-8', sep = ',')