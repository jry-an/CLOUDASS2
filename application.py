# render_template knows to search into a folder named templates
from flask import Flask, render_template, request
from google.cloud import datastore

# Reference the current module which is application.py
app = Flask(__name__)

datastore_client = datastore.Client()

kind = 'News'


def new_news(id, title, content):
    entity = datastore.Entity(key=datastore_client.key(kind, id))

    # create new news post
    entity['title'] = title.decode('utf-8')
    entity['content'] = content.decode('utf-8')
    datastore_client.put(entity)


# The URL endpoint for a particular a thing in the app.
@app.route("/", methods=['GET'])
def home():
    
    query = datastore_client.query(kind=kind)
    news_list = list(query.fetch())
    return render_template('home.html', news_list=news_list)

# render news page to enter a new post
@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/news', methods=['GET','POST'])
def news_post():
    # get title and content from html
    news_title = request.form['title']
    news_content = request.form['content']
    
    # post new news to datastore entity
    new_news(1, news_title, news_content)

    return render_template('home.html')

    





if __name__ == "__main__":
    # If we have any errors it'll pop up on the website
    app.run(debug=True)
