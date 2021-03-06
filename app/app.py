#calling DATABASE methods

import psycopg2
import time
import flask
import json
import sqlite3
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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/", methods=["GET","POST"])
def index_page():
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
            return render_template("index.html", name=name, cuisine=cuisine, address=address, price_range=price_range, webpage=webpage, opening_times=opening_times)
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

@app.route("/deals", methods=["GET", "POST"])
def deals_page():
    return render_template("deals.html")


@app.route("/search_results")
def search_results():
    pass


@app.route('/api/places/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('places.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM places;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/places', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')
    cuisine = query_parameters.get('cuisine')
    address = query_parameters.get('address')
    price_range = query_parameters.get('price_range')
    webpage = query_parameters.get('webpage')
    opening_times = query_parameters.get('opening_times')

    query = "SELECT * FROM places WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if name:
        query += ' name=? AND'
        to_filter.append(name)
    if cuisine:
        query += ' cuisine=? AND'
        to.filter.append(cuisine)
    if address:
        query += ' address=? AND'
        to_filter.append(address)
    if price_range:
        query += ' price_range=? AND'
        to_filter.append(price_range)
    if webpage:
        query += ' webpage=? AND'
        to_filter.append(webpage)
    if opening_times:
        query += ' opening_times=? AND'
        to_filter.append(opening_times)
    if not (id or name or cuisine or address or price_range or webpage or opening_times):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('places.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


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
    sql = """INSERT INTO places(name, cuisine, address, price_range, webpage, opening_times)
    VALUES(?, ?, ?, ?, ?, ?)"""
    # cursor.execute(postgres_insert_query, 
    # (name, cuisine, address, price_range, webpage, opening_times))
    # print("inserted into Database")   

    conn = sqlite3.connect('places.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    db_return = cur.execute(sql, (name, cuisine, address, price_range, webpage, opening_times))
    conn.commit()
    print("inserted into Database")

def retrieve_from_db(name):
    
    sql_return_query = """SELECT * FROM places WHERE name = ?"""

    param = config()
    conn = sqlite3.connect('places.db')
    cur = conn.cursor()
    cur.execute(sql_return_query, (name,))
    print(cur.fetchone())
    

    results_objects = sjdkljsdjs
    return json.dumps(results_objects)

    cur.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
