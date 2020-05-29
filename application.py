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
from pythonTemplate import NewsClass

# Twitter API
from pythonTemplate import twitterAPI

# autoML Translate
from autoMLTranslate import translate_predict

# Class Clients
uniClass = MySQLClass.universities()
food_class = BigQueryClass.Food_Coordinations()
twitter_class = BigQueryClass.Tweet_List()
newsClass = NewsClass


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le0ffoUAAAAABDLaqsF0lFapZWJETkNjq6iRLJS'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le0ffoUAAAAADKNzRynp6vL2atQ40XojYNTtW20'


    ################ FILE FUNCTIONS ####################
# obtain table from BigQuery and append to textfile
tweet_query_result = BigQueryClass.Tweet_List.file_append()

#   Translate tweet messages to spanish by using the trained model
translate_predict.Translate_File.translating()

class LoginForm(FlaskForm):
    recaptcha = RecaptchaField()

@app.route("/", methods=['GET', 'POST'])
def index():
    translate_result = []
    with open('translated_text.txt', 'r') as file:
                content = file.read()
                translate_result.append(content)

    return render_template('home.html', universities=uniClass.uni, rows=food_class.locations, twitter_list=tweet_query_result, news_list=newsClass.query(), translated=translate_result)

# render news page to enter a new post
@app.route('/news')
def news():
    form = LoginForm()
    return render_template('news.html', form=form)



@app.route('/news', methods=['GET', 'POST'])
def news_post():
    form = LoginForm()

    if form.validate_on_submit():
        # get title and content from html
        news_title = request.form['title']
        news_content = request.form['content']
        # post new news to datastore entity
        newsClass.new_news(news_title, news_content)
        return redirect(url_for('index'), code=303)

    return render_template('news.html', form=form)

if __name__ == "__main__":
    
    twitter_data = []

    ############### PUBLISHING TO PUB/SUB ###############
    # Reference to twitter class
    # twitter_client = twitterAPI.TwitterClient('university')

    # # Reference to specified format
    # Tweets = twitter_client.get_most_recent_tweets(10)

    # # Put Json Results into array for publishing
    # for item in Tweets:
    #     twitter_data.append(item)

    # # Convert array into JSON data
    # json.dumps(twitter_data, indent=4, sort_keys=True, default=str)

    # # Publish real-time twitter messages to pub/sub
    # publish_messages('cloudcoursedelivery', 'tweet', twitter_data)
  

    app.run(host='localhost', debug=True, use_reloader=False)
