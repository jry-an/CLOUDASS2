from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitterCredentials
import json
# TWITTER CLIENT
class TwitterClient():

    # if twitter user is not specified the default value is none, in other words your own tweets
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_most_recent_tweets(self, num_tweets):
        recent_tweets = []
        new_search = '#university -filter:retweets'
        tweets = Cursor(self.twitter_client.home_timeline, q=new_search, id=self.twitter_user, exclude_replies=True).items(num_tweets)
        recent_tweets = [[tweet.created_at, tweet.user.screen_name, tweet.text] for tweet in tweets]


        # with open('test.json', 'a', encoding='utf8') as file:
        #         json.dump(recent_tweets._json, file, indent = 4)
        return recent_tweets

# TWITTER AUTHENTICATOR
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitterCredentials.CONSUMER_KEY, twitterCredentials.CONSUMER_SECRET)
        auth.set_access_token(twitterCredentials.ACCESS_TOKEN, twitterCredentials.ACCESS_TOKEN_SECRET)
        return auth


# Class for streaming and processing live tweets
class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator

    def stream_tweets(self, fetched_tweets, hash_tag_list):

        # complete authentication process
        listener = TwitterListener(fetched_tweets)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        # Passing in auth to verify, and listener is responsible is how to deal with the data and error
        stream = Stream(auth, listener)
        
        # Takes in a list of things that if the tweet contains any of the these objects, it'll apply it to the stream
        stream.filter(track=hash_tag_list)


# A Class that prints received tweets to stdout
class TwitterListener(StreamListener):

    # Constructor (Fetched_tweets, is the variable to write the tweets to)
    def __init__(self, fetched_tweets):
        self.fetched_tweets = fetched_tweets

    # Takes in data that is streamed from streamListener the one that is listening for tweets
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    # Occurs if error is present
    def on_error(self, status):
        if status == 420:
            # Returning False on data method in case rate limit occurs.
            return False
        print(status)
