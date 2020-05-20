from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# cafe_name_query = """SELECT Trading_name, MIN(Block_ID) FROM `cloudcoursedelivery.food.food_location` GROUP BY Trading_name"""
# cafe_array = [dict(row) for row in cafe_rows]

class Food_Coordinations:
        query = """SELECT latitude, longitude, MIN(Block_ID) FROM `cloudcoursedelivery.food.food_location` GROUP BY latitude, longitude"""
        locationExecute = client.query(query)  # Make an API request
        locations = [dict(row) for row in locationExecute]

class Tweet_List:
        tweet_query = """SELECT payloadString FROM `cloudcoursedelivery.bqTweets.tweeting_error_records`"""
        t_listExecute = client.query(tweet_query)  # Make an API request
        twitter_list = [dict(row) for row in t_listExecute]