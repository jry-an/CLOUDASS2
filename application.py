from flask import Flask, render_template, request, url_for, redirect
from google.appengine.ext import ndb


class News(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)


# Reference the current module which is application.py
app = Flask(__name__)

# example information to test map API, I will update this with Google cloud MYSQL
class School:
    def __init__(self, key, name, lat, lng):
        self.key  = key # Identifier for each object
        self.name = name
        self.lat  = lat
        self.lng  = lng

universities = (
    School('rmit',      'RMIT',   -37.808125, 144.962701),
    School('monash', 'Monash',    -37.910545, 145.136246),
    School('sb',     'Swinburne', -37.822146, 145.038955)
)

# lookup by key by creating a dictionary, for every object in universities
# we create a school object inside uni_by_key
uni_by_key = {school.key: school for school in universities}

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
    return render_template('home.html', news_list=news_list, universities=universities)

# Anything following the / is to be passed into the function below
@app.route("/<school_code>")

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
# Using the passed in variable school_code into the function
def show_school(school_code):

    # Using school_code to lookup in the uni_by_key dictionary
    school = uni_by_key.get(school_code)

    # If Found
    if school:
        return render_template('map.html', school=school)

    # If not found (Page not found)
    else:
        abort(404)

if __name__ == "__main__":
    # If we have any errors it'll pop up on the website
    app.run(debug=True)
