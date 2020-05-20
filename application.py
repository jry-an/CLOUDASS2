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

# DataFlow Libraries
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
# Regular Expressions
import re
import sys


# Class Clients
uniClass = MySQLClass.universities()
locationClass = BigQueryClass.Food_Coordinations()

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('home.html', universities=uniClass.uni, rows=locationClass.locations)


if __name__ == "__main__":
    twitter_data = []

    # # RMIT
    # Reference to twitter class
    twitter_clientRMIT = twitterAPI.TwitterClient('RMIT')
    # Reference to specified format
    # RMITTweets = twitter_clientRMIT.get_most_recent_tweets(10)
    
    # Put Json Results into array for Inserting into BigQuery
    for item in RMITTweets:
        twitter_data.append(item.created_at)
        twitter_data.append(item.user.description)
        twitter_data.append(item.user.screen_name)

    # print(twitter_data)

    # Publish real-time twitter messages
    publish_messages('cloudcoursedelivery', 'tweets', twitter_data)
    # Use Pipeline to read from pub messages and output to text file
    
    # Receive real-time twitter messages
    # receive_messages('cloudcoursedelivery', 'MySub', 10)


    app.run(host='localhost', debug=True)

