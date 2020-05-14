# render_template knows to search into a folder named templates
from flask import Flask, render_template, url_for, redirect
from decimal import *

import mysql.connector

# import mysql.connector
# import MySQLdb
# Grab connection to MySQL workbench which connects to Google Cloud SQL database
mydb = mysql.connector.connect(host="35.197.188.118", user="aaron", passwd="", database="universities", port=3306)
# mydb = MySQLdb.connect(host="35.197.188.118", user="aaron", passwd="", database="universities")


# Connect to the database
# mydb = pymysql.connect(host="35.197.188.118", user="aaron", passwd="", database="universities")

# Reference the current module which is application.py
app = Flask(__name__)

# Class that holds Database information for Google Map API
class School:
    def __init__(self, key, name, lat, lng):
        self.key  = key # Identifier for each object
        self.name = name
        self.lat  = lat
        self.lng  = lng

# Retrieve Data from row 1
row1 = mydb.cursor()
row1.execute("SELECT * FROM universities.school WHERE (`key` = '1');")
row1Result = row1.fetchone()
row1NumID = str(row1Result[0])
row1Name = str(row1Result[1])
row1Lat = Decimal(row1Result[2])
row1Lng = Decimal(row1Result[3])

# Retrieve Data from row 2
row2 = mydb.cursor()
row2.execute("SELECT * FROM universities.school WHERE (`key` = '2');")
row2Result = row2.fetchone()
row2NumID = str(row2Result[0])
row2Name = str(row2Result[1])
row2Lat = Decimal(row2Result[2])
row2Lng = Decimal(row2Result[3])

# Retrieve Data from row 3
row3 = mydb.cursor()
row3.execute("SELECT * FROM universities.school WHERE (`key` = '3');")
row3Result = row3.fetchone()
row3NumID = str(row3Result[0])
row3Name = str(row3Result[1])
row3Lat = Decimal(row3Result[2])
row3Lng = Decimal(row3Result[3])

# Array for all created objects
universities = (
    School(row1NumID,      row1Name,   row1Lat, row1Lng),
    School(row2NumID, row2Name,    row2Lat, row2Lng),
    School(row3NumID,     row3Name, row3Lat, row3Lng)
)

# lookup by key by creating a dictionary, for every object in universities
# we create a school object inside uni_by_key
uni_by_key = {school.key: school for school in universities}

@app.route("/")
def index():
    # fetch all database names in our machine
    mycursor = mydb.cursor()

    mycursor.execute("select name from school")

    result = mycursor.fetchall()

    # Passing in schools tuples
    return render_template('home.html', universities=universities, results=result)

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

if __name__ == "__main__":

    app.run(host='localhost', debug=True)