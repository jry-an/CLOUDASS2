# render_template knows to search into a folder named templates
from flask import Flask, current_app, render_template, request, redirect, url_for

# reCaptcha
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf
import json
from google.cloud import pubsub_v1
import os

# Cohesive classes
from pythonTemplate import BigQueryClass
from pythonTemplate import MySQLClass
from pythonTemplate import reviewClass

# Twitter API
from pythonTemplate import twitterAPI

# autoML Translate
from autoMLTranslate import translate_predict

# Class Clients
uniClass = MySQLClass.universities()
food_class = BigQueryClass.Food_Coordinations()
twitter_class = BigQueryClass.Tweet_List()
review_class = reviewClass


app = Flask(__name__)

# reCAPTCHA authenticaton
app.config['SECRET_KEY'] = 'PersonalSecretKey!'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le0ffoUAAAAABDLaqsF0lFapZWJETkNjq6iRLJS'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le0ffoUAAAAADKNzRynp6vL2atQ40XojYNTtW20'

# Pub/Sub Verificaiton 
app.config['PUBSUB_VERIFICATION_TOKEN'] = \
    os.environ['PUBSUB_VERIFICATION_TOKEN']
app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']
app.config['PROJECT'] = os.environ['GOOGLE_CLOUD_PROJECT']

# STEP 1: Retrive Tweet data
twitter_data = []
twitter_client = twitterAPI.TwitterClient('university')
Tweets = twitter_client.get_most_recent_tweets(4)

# Put Json Results into array for publishing
for item in Tweets:
    twitter_data.append(item)
# Convert array into JSON data
json.dumps(twitter_data, indent=4, sort_keys=True, default=str)

# STEP 2: Push Tweet data to Publisher (pub/sub service)
publisher = pubsub_v1.PublisherClient()


# STEP 3: Use Dataflow to convert tweet data into BigQuery tables
tweet_query_result = BigQueryClass.Tweet_List.file_append()


# STEP 5: Use autoML trained model to predict the english text into the selected language (spanish)
translated_result = translate_predict.sample_translate_text_with_model('TRL4666006290886033408', tweet_query_result, 'es', 'en', 'cloudcoursedelivery', 'us-central1', )



@app.route("/", methods=['GET', 'POST'])
def index():

    #  Authentication for pub/sub
    topic_path = publisher.topic_path(current_app.config['PROJECT'],
        current_app.config['PUBSUB_TOPIC'])

    # A loop that publishes each twitter data into publisher
    for n in twitter_data:
        data = u"{}".format(n)
        print(n)
        # Data must be a bytestring
        data = data.encode("utf-8")
        # When you publish a message, the client returns a future.
        publisher.publish(topic_path, data=data)

    return render_template('home.html'
                           ,universities=uniClass.uni,
                                         rows=food_class.locations,
                                          twitter_list=tweet_query_result,
                                          translated_text=translated_result,
                                            twitter_data=twitter_data,
                                           review_list=review_class.query())

@app.route('/review')
def news():
    return render_template('review.html')


@app.route('/review', methods=['GET', 'POST'])
def news_post():

    # get title and content from html
    name = request.form['name']
    review = request.form['review']
    # post new news to datastore entity
    review_class.new_reviews(name, review)
    return redirect(url_for('index'), code=303)
                       


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', debug=True)
# [END gae_python37_app]
