# render_template knows to search into a folder named templates
from flask import Flask, render_template, url_for

# Reference the current module which is application.py
app = Flask(__name__)

# The URL endpoint for a particular a thing in the app.
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

if __name__ == "__main__":

    # If we have any errors it'll pop up on the website
    app.run(debug=True)