# render_template knows to search into a folder named templates
from flask import Flask, render_template, request, redirect, url_for

import BigQueryClass
import MySQLClass
import NewsClass
# Cohesive classes
import twitterAPI

# Pub/Sub classes
# from publish import publish_messages

<<<<<<< HEAD

# Class Clients
uniClass = MySQLClass.universities()
food_class = BigQueryClass.Food_Coordinations()
twitter_class = BigQueryClass.Tweet_List()
newsClass = NewsClass



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('home.html', universities=uniClass.uni, rows=locationClass.locations, news_list=newsClass.query())


<<<<<<< HEAD
    return render_template('home.html', universities=uniClass.uni, rows=food_class.locations, twitter_list=twitter_class.twitter_list)

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
    newsClass.new_news(news_title, news_content)
    return redirect(url_for('index'), code=303)

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
