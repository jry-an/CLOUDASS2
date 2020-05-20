# render_template knows to search into a folder named templates
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import datastore

import BigQueryClass
import MySQLClass
# Cohesive classes
import twitterAPI
import datetime

# Pub/Sub classes
# from publish import publish_messages

# DataFlow Libraries
# Regular Expressions


# Class Clients
uniClass = MySQLClass.universities()
locationClass = BigQueryClass.Food_Coordinations()
datastore_client = datastore.Client()
kind = 'News'


def new_news(title, content):
    entity = datastore.Entity(key=datastore_client.key(kind))
    entity['title'] = title
    entity['content'] = content
    entity['time'] = datetime.datetime.now()
    datastore_client.put(entity)


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    query = datastore_client.query(kind=kind)
    query.order = ['-time']
    news_list = list(query.fetch())
    return render_template('home.html', universities=uniClass.uni, rows=locationClass.locations, news_list=news_list)


# render news page to enter a new post
@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/news', methods=['GET', 'POST'])
def news_post():
    # get title and content from html
    news_title = request.form['title']
    news_content = request.form['content']

    # post new news to datastore entity
    new_news(news_title, news_content)

    return redirect(url_for('index'), code=303)

if __name__ == "__main__":
    twitter_data = []

    # # RMIT
    # Reference to twitter class
    twitter_clientRMIT = twitterAPI.TwitterClient('RMIT')
    # Reference to specified format
    RMITTweets = twitter_clientRMIT.get_most_recent_tweets(10)

    # Put Json Results into array for Inserting into BigQuery
    for item in RMITTweets:
        twitter_data.append(item.created_at)
        twitter_data.append(item.user.description)
        twitter_data.append(item.user.screen_name)

    # print(twitter_data)

    # Publish real-time twitter messages
    # publish_messages('cloudcoursedelivery', 'tweets', twitter_data)
    # Use Pipeline to read from pub messages and output to text file

    # Receive real-time twitter messages
    # receive_messages('cloudcoursedelivery', 'MySub', 10)

    app.run(host='localhost', debug=True)
