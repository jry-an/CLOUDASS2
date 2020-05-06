# render_template knows to search into a folder named templates
from flask import Flask, render_template
from google.cloud import datastore

# Reference the current module which is application.py
app = Flask(__name__)

datastore_client = datastore.Client()

kind = 'User'

def new_user(id, name, password):
    entity = datastore.Entity(key=datastore_client.key(kind, id))
    # TODO - check if user id already exists

    # create new user
    entity['name'] = name.decode('utf-8')
    entity['password'] = password.decode('utf-8')
    datastore_client.put(entity)


# The URL endpoint for a particular a thing in the app.
@app.route("/")
def home():
    # Store the current access time in Datastore.
    new_user(3,'Jeff','password')

    # Fetch the most recent 10 access times from Datastore.

    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/salvador")
def salvador():
    return "Hello, Salvador"


if __name__ == "__main__":
    # If we have any errors it'll pop up on the website
    app.run(debug=True)
