# render_template knows to search into a folder named templates
from flask import Flask, render_template, url_for, redirect
import sqlalchemy

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


@app.route("/")
def index():

    # Passing in schools tuples
    return render_template('home.html', universities=universities)

# Anything following the / is to be passed into the function below
@app.route("/<school_code>")

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

app.run(host='localhost', debug=True)