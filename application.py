# render_template knows to search into a folder named templates
from flask import Flask, render_template, url_for, redirect, request
from decimal import *
import mysql.connector
import os
from google.cloud import bigquery
from google.cloud import pubsub_v1

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

# DataFlow (incomplete)
def dataFlow(argv=None):
        sys.setrecursionlimit(2000)
        with app.test_request_context():
            """Build and run the pipeline."""
            parser = argparse.ArgumentParser()
            parser.add_argument(
                '--topic',
                type=str,
                help='Pub/Sub topic to read from')
            parser.add_argument(
                '--output',
                help=('Output local filename'))
            args, pipeline_args = parser.parse_known_args(argv)
            options = PipelineOptions(pipeline_args)
            options.view_as(StandardOptions).runner = 'DataflowRunner'
            google_cloud_options = options.view_as(GoogleCloudOptions)
            google_cloud_options.project = 'cloudcoursedelivery'
            google_cloud_options.job_name = 'myjob'
            google_cloud_options.staging_location = 'gs://tweets-au-bucket'
            google_cloud_options.temp_location = 'gs://aarontempbucket'
            google_cloud_options.region = 'australia-southeast1'
            options.view_as(SetupOptions).save_main_session = True

            # Streaming python
            options.view_as(StandardOptions).streaming = True

            # P constructs the pipeline
            p = beam.Pipeline(options=options)
            (p  | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic=args.topic,
                    id_label="MESSAGE_ID")
                | 'Write to file' >> beam.io.WriteToText(args.output)
            )

            result = p.run()
            # Important for streaming, running it forever until its stopped
            result.wait_until_finish()
    

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('home.html', universities=uniClass.uni, rows=locationClass.locations)


if __name__ == "__main__":
    twitter_data = []

    # Reference to twitter class
    twitter_client = twitterAPI.TwitterClient('RMIT')
    # Reference to specified format
    resultArray = twitter_client.get_most_recent_tweets(5)

    # Put Json Results into array for Inserting into BigQuery
    for item in resultArray:
        twitter_data.append(item.text)
    # print(valuable_data)

    # Publish real-time twitter messages
    publish_messages('cloudcoursedelivery', 'tweets', twitter_data)
    # Use Pipeline to read from pub messages and output to text file
    dataFlow()
    
    # Receive real-time twitter messages
    receive_messages('cloudcoursedelivery', 'MySub', 10)


    app.run(host='localhost', debug=True)

