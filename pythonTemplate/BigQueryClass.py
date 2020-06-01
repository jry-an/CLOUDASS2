from google.cloud import bigquery
import os
import json

# Construct a BigQuery client object.
client = bigquery.Client()

class Food_Coordinations:
        query = """SELECT latitude, longitude, MIN(Block_ID) FROM `cloudcoursedelivery.food.food_location` GROUP BY latitude, longitude"""
        locationExecute = client.query(query)  # Make an API request
        locations = [dict(row) for row in locationExecute]


class Tweet_List:
        twitter_list = []
        def file_append():
                tweet_query = """SELECT payloadString FROM `cloudcoursedelivery.bqTweets.tweeting_error_records` LIMIT 5"""
                t_listExecute = client.query(tweet_query)  # Make an API request
                twitter_list = [dict(row) for row in t_listExecute]
                # Creates a new txt file if its non-existent, else overwrites content
                # with open('translated_text.txt', 'w') as file:
                #         file.write(json.dumps(twitter_list))

                return twitter_list