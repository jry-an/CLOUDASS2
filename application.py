# render_template knows to search into a folder named templates
from flask import Flask, render_template, url_for, redirect
from decimal import *
import mysql.connector
import sqlalchemy
import os
from google.cloud import bigquery
import json

from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from google.cloud import pubsub_v1

import twitterCredentials


# TWITTER CLIENT
class TwitterClient():

    # if twitter user is not specified the default value is none, in other words your own tweets
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friendlist(self, num_friends):
        friends_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_most_recent_tweets(self, num_tweets):
        recent_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            recent_tweets.append(tweet)

            with open('test.json', 'a', encoding='utf8') as file:
                json.dump(tweet._json, file, indent = 4)

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

# Grab connection to MySQL workbench which connects to Google Cloud SQL database
mydb = mysql.connector.connect(host="35.197.188.118", user="aaron", passwd="aaron", database="universities", port=3306)


# mydb = MySQLdb.connect(host="35.197.188.118", user="aaron", passwd="", database="universities")
# mydb = mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>
# mydb = pymysql.connect(host="35.197.188.118", user="aaron", passwd="", database="universities")

# Reference the current module which is application.py
app = Flask(__name__)

# Class that holds Database information for Google Map API
class School:
    def __init__(self, key, name, lat, lng):
        self.key  = key # Identifier for each object
        self.name = name
        self.lat  = lat
        self.lng  = lng

# Retrieve Data from row 1
row1 = mydb.cursor()
row1.execute("SELECT * FROM universities.school WHERE (`key` = '1');")
row1Result = row1.fetchone()
row1NumID = str(row1Result[0])
row1Name = str(row1Result[1])
row1Lat = Decimal(row1Result[2])
row1Lng = Decimal(row1Result[3])

# Retrieve Data from row 2
row2 = mydb.cursor()
row2.execute("SELECT * FROM universities.school WHERE (`key` = '2');")
row2Result = row2.fetchone()
row2NumID = str(row2Result[0])
row2Name = str(row2Result[1])
row2Lat = Decimal(row2Result[2])
row2Lng = Decimal(row2Result[3])

# Retrieve Data from row 3
row3 = mydb.cursor()
row3.execute("SELECT * FROM universities.school WHERE (`key` = '3');")
row3Result = row3.fetchone()
row3NumID = str(row3Result[0])
row3Name = str(row3Result[1])
row3Lat = Decimal(row3Result[2])
row3Lng = Decimal(row3Result[3])

# Array for all created objects
universities = (
    School(row1NumID,      row1Name,   row1Lat, row1Lng),
    School(row2NumID, row2Name,    row2Lat, row2Lng),
    School(row3NumID,     row3Name, row3Lat, row3Lng)
)

# lookup by key by creating a dictionary, for every object in universities
# we create a school object inside uni_by_key
uni_by_key = {school.key: school for school in universities}

# Construct a BigQuery client object.
client = bigquery.Client()

query = """SELECT latitude, longitude, MIN(Block_ID) FROM `cloudcoursedelivery.food.food_location` GROUP BY latitude, longitude"""
cafe_name_query = """SELECT Trading_name, MIN(Block_ID) FROM `cloudcoursedelivery.food.food_location` GROUP BY Trading_name"""
rows = client.query(query)  # Make an API request
cafe_rows = client.query(cafe_name_query)

coord = [dict(row) for row in rows]
cafe_array = [dict(row) for row in cafe_rows]






@app.route("/")
def index():
    # fetch all database names in our machine
    mycursor = mydb.cursor()
    mycursor.execute("select name from school")
    result = mycursor.fetchall()
    




    # Passing in schools tuples
    return render_template('home.html', universities=universities, results=result, rows=coord, cafe = cafe_array)

# Anything following the / is to be passed into the function below
@app.route("/map")
def run():
    return render_template('map.html', rows=coord, universities=universities)



if __name__ == "__main__":

    hash_tag_list = ["RMIT", "UniMelb", "Victoria University"]

    fetched_tweets = "test.json"

    twitter_client = TwitterClient('RMIT')
    resultArray = twitter_client.get_most_recent_tweets(5)

    # Put Json Results into array for Inserting into BigQuery
    valuable_data = []
    for item in resultArray:
        valuable_data.append(item.text)
    print(valuable_data)


    app.run(host='localhost', debug=True)
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets, hash_tag_list)
