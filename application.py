from flask import Flask, render_template, request
from google.appengine.ext import ndb


class News(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)


# Reference the current module which is application.py
app = Flask(__name__)


def new_news(title, content):
    new = News()
    new.title = title.decode('utf-8')
    new.content = content.decode('utf-8')
    new.put()


# The URL endpoint for a particular a thing in the app.
@app.route("/", methods=['GET'])
def home():
    # Store the current access time in Datastore.
    query = News.query()
    news_list = query.fetch(10)
    return render_template('home.html', news_list=news_list)


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

    return render_template('home.html')


if __name__ == "__main__":
    # If we have any errors it'll pop up on the website
    app.run(debug=True)
