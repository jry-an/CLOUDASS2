# render_template knows to search into a folder named templates
from flask import Flask, render_template, request, redirect, url_for

# reCaptcha
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf
import json


# Cohesive classes
from pythonTemplate import BigQueryClass
from pythonTemplate import MySQLClass
from pythonTemplate import reviewClass
from pythonTemplate import publish

# Twitter API
from pythonTemplate import twitterAPI

# autoML Translate
# from autoMLTranslate import translate_predict

# Class Clients
uniClass = MySQLClass.universities()
# food_class = BigQueryClass.Food_Coordinations()
twitter_class = BigQueryClass.Tweet_List()
# review_class = reviewClass


app = Flask(__name__)

# reCAPTCHA authenticaton
app.config['SECRET_KEY'] = 'PersonalSecretKey!'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le0ffoUAAAAABDLaqsF0lFapZWJETkNjq6iRLJS'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le0ffoUAAAAADKNzRynp6vL2atQ40XojYNTtW20'

# STEP 1: Retrive Tweet data
twitter_data = []
# twitter_client = twitterAPI.TwitterClient('university')
# Tweets = twitter_client.get_most_recent_tweets(10)

# Put Json Results into array for publishing
# for item in Tweets:
#     twitter_data.append(item)
# # Convert array into JSON data
# json.dumps(twitter_data, indent=4, sort_keys=True, default=str)



# STEP 2: Push Tweet data to Publisher (pub/sub service)
# publish.publish_messages('cloudcoursedelivery', 'tweet', twitter_data)



# STEP 3: Use Dataflow to convert tweet data into BigQuery tables
tweet_query_result = BigQueryClass.Tweet_List.file_append()



# STEP 4: Retrieve BigQuery tweet data column and append inside a textfile (executed inside BigQuery python file)

# STEP 5: Use autoML trained model to predict the english text into the selected language (spanish)
# and append/overrite existing textfile
# translate_predict.Translate_File.translating()



# STEP 6: Output translated data onto webpage
translate_result = []
with open('translated_text.txt', 'r') as file:
            content = file.read()
            translate_result.append(content)

class reCAPTCHA(FlaskForm):
    recaptcha = RecaptchaField()

@app.route("/")
def index():
    return render_template('home.html'
                           # ,
                           # universities=0,
                           #               rows=0,
                                          ,twitter_list=tweet_query_result,
                           #                 review_list=review_class.query(),
                           #                  translated=0
                           )

@app.route('/review')
def news():
    form = reCAPTCHA()
    return render_template('review.html'
                           , form = form
                           )


@app.route('/review', methods=['GET', 'POST'])
def news_post():
    form = reCAPTCHA()

    if form.validate_on_submit():
        # get title and content from html
        name = request.form['name']
        review = request.form['review']
        # post new news to datastore entity
        # review_class.new_reviews(name, review)
        return redirect(url_for('index'), code=303)

    return render_template('review.html'
                           , form=form
                           )


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', debug=True)
# [END gae_python37_app]
