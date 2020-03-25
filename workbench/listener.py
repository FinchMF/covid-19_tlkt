from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt


import config


#-------# A U T H E N T I C A T I O N #-------#

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_token_secret)
        return auth


#-------# C L I E N T #-------#

class Twitter_cli():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.client
    
    def get_user_timeline_tweets(self, num_tw):
        tweets = []
        for tw in Cursor(self.client.user_timeline, id=self.twitter_user).items(num_tw):
            tweets.append(tw)
        return tweets

#-------# S T R E A M  T W E E T S #-------#

class Streamer():

    def __init__(self):
        self.twitter_auth = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, track_list):
        listener = Listener(fetched_tweets_filename)
        auth = self.twitter_auth.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=track_list)



#-------# L I S T E N  T O  S T R E A M #-------#

class Listener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on_data %s' % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False
        print(status)

#-------# A N A L Y Z E R #-------#

class Analyzer():

    def tweets_to_df(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df



if __name__ == '__main__':
    
    twitter_cli = Twitter_cli()
    twitter_analyzer = Analyzer()

    api = twitter_cli.get_twitter_client_api()

    tweets = api.user_timeline(screen_name='realDonaldTrump', count=200)

    df = twitter_analyzer.tweets_to_df(tweets)

    print(np.mean(df['len']))
    print(np.max(df['likes']))
    print(np.max(df['retweets']))

    print(df.head(10))

    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16,4), label='likes', legend=True)

    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_retweets.plot(figsize=(16,4), label='retweets', legend=True)

    plt.show()