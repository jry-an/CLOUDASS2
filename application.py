# render_template knows to search into a folder named templates
from flask import Flask, render_template, url_for, redirect, request
from decimal import *
import mysql.connector
import os
from google.cloud import bigquery
from google.cloud import pubsub_v1
import json

# Cohesive classes
import twitterAPI
import MySQLClass
import BigQueryClass

# Pub/Sub classes
from publish import publish_messages
from receive import receive_messages


# Class Clients
uniClass = MySQLClass.universities()
food_class = BigQueryClass.Food_Coordinations()
twitter_class = BigQueryClass.Tweet_List()


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('home.html', universities=uniClass.uni, rows=food_class.locations, twitter_list=twitter_class.twitter_list)


if __name__ == "__main__":
    
    twitter_data = []

    # Reference to twitter class
    twitter_client = twitterAPI.TwitterClient('university')
    # Reference to specified format
    Tweets = twitter_client.get_most_recent_tweets(10)
    
    # Put Json Results into array for publishing
    for item in Tweets:
        twitter_data.append(item)

    # Convert array into JSON data
    json.dumps(twitter_data, indent=4, sort_keys=True, default=str)
    # print(twitter_data)

    # Publish real-time twitter messages to pub/sub
    publish_messages('cloudcoursedelivery', 'tweet', twitter_data)
    
    # Receive real-time twitter messages
    # receive_messages('cloudcoursedelivery', 'MySub', 10)


    app.run(host='localhost', debug=True)

