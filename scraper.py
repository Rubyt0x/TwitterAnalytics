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
            parsed_tweet['likes'] = tweet.favorite_count
            parsed_tweet['retweets'] = tweet.retweet_count

            all_tweets.append(parsed_tweet)
    
    df = pd.DataFrame(all_tweets)
    df = df.drop_duplicates("text", keep = 'first')

    return df
            
Fuel = get_tweets_from_user("fuellabs_")

print("Data Shape: {}".format(Fuel.shape))

Fuel.to_csv('Fuel_tweets.csv', encoding='UTF-8', sep = ',')








"""my_tweets = api.user_timeline()

columns = ['Time', 'User', 'Tweet', 'Likes', 'Retweets']
data = []
for tweet in my_tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text, tweet.favorite_count, tweet.retweet_count])

df = pd.DataFrame(data, columns = columns)

df.to_csv('April_results.csv')"""





"""#access to my tweets
my_tweets = api.user_timeline()

# Setting up the timezone
lisbon = pytz.timezone('Europe/Lisbon')

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api=None):
        pass

    def stream_tweets(self, filename):
        listener = StdOutListener(filename)
        stream(auth, listener)


    def on_status(self, status):

        #If the tweet is a retweet
        if hasattr(status, 'retweeted_status'):
            print('retweet')
            retweet = 1

            #get a link for each tweet
            link = "https://twitter.com/" + str(status.retweeted_status.user.screen_name) + "/status/" + str(status.retweeted_status.id)
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'html5lib')

            #Replies
            replies = soup.find('span', {"class": "ProfileTweet-actionCount"})
            if replies is not None:
                num_replies = int(replies['data-tweet-stat-count'])
            else:
                num_replies = 0
            
            #Retweets
            li = soup.find('li', {"class": "js-stat-retweets"})
            if li is not None:
                retweets = li.find('a')
                num_retweets = retweets['data-tweet-stat-count']
            else:
                num_retweets = 0
        
            #Favorites
            li2 = soup.find('li', {"class": "js-stat-favorites"})
            if li2 is not None:
                favorites = li2.find('a')
                num_favorites = favorites['data-tweet-stat-count']
            else:
                num_favorites = 0

            #Better Date Format
            central_date = lisbon.localize(status.retweeted_status.created_at)
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            
            #open the results file and stores it to csvFile
            #newline deletes the extra row inbetween lines
            csvFile = open('results.csv', 'a', newline = '')
            csvWriter = csv.writer(csvFile)
            #write the information we want to a csv
            csvWriter.writerow([central_date.strftime(fmt), status.retweeted_status.user.screen_name, 
                                status.retweeted_status.user.followers_count, num_retweets, num_favorites, 
                                num_replies, status.id, retweet, link])
            csvFile.close()

        else:
            #print that it's a regular tweet
            print('tweet')
            retweet = 0
            
            #get a unique link for each tweet
            link = "https://twitter.com/" + str(status.user.screen_name) + "/status/" + str(status.id)
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'html5lib')
            
            #Replies
            replies = soup.find('span', {"class": "ProfileTweet-actionCount"})
            if replies is not None:
                num_replies = int(replies['data-tweet-stat-count'])
            else:
                num_replies = 0

            #Retweets
            li = soup.find('li', {"class": "js-stat-retweets"})
            if li is not None:
                retweets = li.find('a')
                num_retweets = retweets['data-tweet-stat-count']
            else:
                num_retweets = 0
        
            #Favorites
            li2 = soup.find('li', {"class": "js-stat-favorites"})
            if li2 is not None:
                favorites = li2.find('a')
                num_favorites = favorites['data-tweet-stat-count']
            else:
                num_favorites = 0
            
            #Better Date Format
            central_date = lisbon.localize(status.created_at)
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            
            #open the results file and stores it to csvFile
            #newline deletes the extra row inbetween lines
            csvFile = open('results.csv', 'a', newline = '')
            csvWriter = csv.writer(csvFile)
            #write the information we want to a csv
            csvWriter.writerow([central_date.strftime(fmt), status.user.screen_name, 
                                status.user.followers_count, num_retweets, num_favorites, num_replies, 
                                status.id, retweet, link])
            csvFile.close()

    def on_error(self, status_code):
        if status_code == 420:
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
"""