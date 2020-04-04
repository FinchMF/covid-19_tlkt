import tweepy 
from tweepy import TweepError
import csv
import config

import time 

#Twitter API credentials
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(screen_name=screen_name,
                                       count=200)

    except TweepError:
        print('limit error on ' + screen_name + 'during intital request')
        print('waiting 15min...')
        time.sleep(900)
        print('waking back up...')
        print('now retrieving tweets from ' + screen_name)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)
        print('retrieved new_tweets list from ' + screen_name)
        

	
	#save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        try:
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        except TweepError:
            print('limit error on ' + screen_name + ' during oldest')
            print('waiting 15min...')
            time.sleep(900)
            print('waking back up...')
            print('now retrieving more tweets from ' + screen_name)
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
            continue
        
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print("...%s tweets downloaded so far" % (len(alltweets)))

    
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text, tweet.retweet_count] for tweet in alltweets]

    #write the csv	
    with open('figure_tweets/%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text","retweet_count"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
    handle_list = ['Acosta'
                   ]	
        
    for handle in handle_list:
            get_all_tweets(handle)
       




