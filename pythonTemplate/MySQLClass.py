from decimal import *
import mysql.connector

# mydb = mysql.connector.connect(host="35.197.188.118", user="aaron", passwd="aaron", database="universities", port=3306)

# Class that holds Database information for Google Map API
class School:
    def __init__(self, key, name, lat, lng):
        self.key  = key # Identifier for each object
        self.name = name
        self.lat  = lat
        self.lng  = lng

class universities:
    i = 0
    # # Retrieve Data from row 1
    # row1 = mydb.cursor()
    # row1.execute("SELECT * FROM universities.school WHERE (`key` = '1');")
    # row1Result = row1.fetchone()
    # row1NumID = str(row1Result[0])
    # row1Name = str(row1Result[1])
    # row1Lat = Decimal(row1Result[2])
    # row1Lng = Decimal(row1Result[3])
    #
    # # Retrieve Data from row 2
    # row2 = mydb.cursor()
    # row2.execute("SELECT * FROM universities.school WHERE (`key` = '2');")
    # row2Result = row2.fetchone()
    # row2NumID = str(row2Result[0])
    # row2Name = str(row2Result[1])
    # row2Lat = Decimal(row2Result[2])
    # row2Lng = Decimal(row2Result[3])
    #
    # # Retrieve Data from row 3
    # row3 = mydb.cursor()
    # row3.execute("SELECT * FROM universities.school WHERE (`key` = '3');")
    # row3Result = row3.fetchone()
    # row3NumID = str(row3Result[0])
    # row3Name = str(row3Result[1])
    # row3Lat = Decimal(row3Result[2])
    # row3Lng = Decimal(row3Result[3])
    #
    #     # Array for all created objects
    # uni = (
    #         School(row1NumID,      row1Name,   row1Lat, row1Lng),
    #         School(row2NumID, row2Name,    row2Lat, row2Lng),
    #         School(row3NumID,     row3Name, row3Lat, row3Lng)
    # )
