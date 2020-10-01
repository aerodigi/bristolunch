import flask
from flask import request, jsonify, render_template, flash
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "6%t6^sl8i3hzozdws*h5fmo#4brcwa**bz01bn0$q57ef7"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

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

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


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


app.run()



# def insert_into_db(name, cuisine, address, price_range, webpage, opening_times):
#     postgres_insert_query = """INSERT INTO details(name, cuisine, address, price_range, webpage, opening_times)
#     VALUES(%s, %s, %s, %s, %s, %s) RETURNING id"""
#     # cursor.execute(postgres_insert_query, 
#     # (name, cuisine, address, price_range, webpage, opening_times))
#     # print("inserted into Database")   

#     param = config()
#     conn = psycopg2.connect(
#         dbname ="bristolunch_test",
#         user="ash",
#         host="localhost", 
#         password="password123")
#     cur = conn.cursor()
#     db_return = cur.execute(postgres_insert_query, (name, cuisine, address, price_range, webpage, opening_times))
#     conn.commit()
#     print("inserted into Database")

#     cur.close()


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
