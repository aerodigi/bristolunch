#calling DATABASE methods

import psycopg2
import time
import flask
import json
from flask import jsonify, Flask, request, redirect, render_template, flash
from configparser import ConfigParser
from config import config
from psycopg2 import connect

app = Flask(__name__)
app.secret_key = "6%t6^sl8i3hzozdws*h5fmo#4brcwa**bz01bn0$q57ef7"

conn = psycopg2.connect(
    host="localhost",
    dbname="bristolunch_test",
    user="ash",
    password="password123")

@app.route("/", methods=["GET","POST"])
def index_page():
    return render_template("index.html")


@app.route("/add_details", methods=["GET", "POST"])
def add_details_page():
    if request.method == "POST":
        place_details = request.form["name"]
        place_details_cuisine = request.form["cuisine"]
        place_details_address = request.form["address"]
        place_details_price_range = request.form["price_range"]
        place_details_webpage = request.form["webpage"]
        place_details_opening_times = request.form["opening_times"]
        insert_into_db(place_details, place_details_cuisine, place_details_address, place_details_price_range, place_details_webpage, place_details_opening_times)
        flash("Added details " + str(place_details) + " to our DB, thanks for your input!")
        return render_template("add_details.html")
    return render_template("add_details.html")


@app.route("/about", methods=["GET"])
def about_page():
    return render_template("about.html")


@app.route("/search_details", methods=["GET", "POST"])
def search_details_page():
    if request.method == "POST":
        result_searchedplace = request.form["searchedplace"]
        db_result = retrieve_from_db('name')
        if db_result == None:
            print("We do not have any information regarding your search on our database.")
            return "0"
        else:
            place_details = dbresult.get["name"]
            place_details_cuisine = dbresult.get["cuisine"]
            place_details_address = dbresult.get["address"]
            place_details_price_range = dbresult.get["price_range"]
            place_details_webpage = dbresult.get["webpage"]
            place_details_opening_times = dbresult.get["opening_times"]
            return render_template("search_details.html", name=name, cuisine=cuisine, address=address, price_range=price_range, webpage=webpage, opening_times=opening_times)
    return render_template("search_details.html")


@app.route("/search_results")
def search_results():
    pass


@app.route("/api/", methods=["GET"])
def api_places():
    places_list = []
    places_name = []
    places_cuisine = []
    places_address = []
    places_price_range = []
    places_webpage = []
    places_opening_times = []
    for document in col.find():
        places_list += document
        places_name.append(document.get("name"))
        places_cuisine.append(document.get("cuisine"))
        places_address.append(document.get("address"))
        places_price_range.append(document.get("price_range"))
        places_webpage.append(document.get("webpage"))
        places_opening_times(document.get("opening_times"))
    return {        
        "Places to Eat": {
                "name": places_name, 
                "cuisine": places_cuisine,
                "platform": places_address,
                "price_range": places_price_range,
                "webpage": places_webpage,
                "opening_times": places_opneing_times,
        }
    }

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():

    conn = None
    try:
        param = config()
        print('Connecting to PostSQL Databased...')
        conn = psycopg2.connect(
            dbname ="bristolunch_test",
            user="ash",
            host="localhost", 
            password="password123")
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()

def insert_into_db(name, cuisine, address, price_range, webpage, opening_times):
    postgres_insert_query = """INSERT INTO details(name, cuisine, address, price_range, webpage, opening_times)
    VALUES(%s, %s, %s, %s, %s, %s) RETURNING id"""
    # cursor.execute(postgres_insert_query, 
    # (name, cuisine, address, price_range, webpage, opening_times))
    # print("inserted into Database")   

    param = config()
    conn = psycopg2.connect(
        dbname ="bristolunch_test",
        user="ash",
        host="localhost", 
        password="password123")
    cur = conn.cursor()
    db_return = cur.execute(postgres_insert_query, (name, cuisine, address, price_range, webpage, opening_times))
    conn.commit()
    print("inserted into Database")

    cur.close()

def retrieve_from_db(name):
    
    postgres_return_query = """SELECT * FROM details WHERE name = %s"""

    param = config()
    conn = psycopg2.connect(
        dbname ="bristolunch_test",
        user="ash",
        host="localhost", 
        password="password123")
    cur = conn.cursor()
    cur.execute(postgres_return_query, (name,))
    print(cur.fetchone())
    

    cur.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
