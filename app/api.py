import flask
from flask import request, jsonify
from config import config
import psycopg2

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Adds data for our catalogue in the form of a list of dictionaries


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




places = [
    {'id': 0,
     'name': 'Al Bab Mansour/Cafe Atlas',
     'cuisine': 'Morrocan',
     'address': 'St Nicholas Market, Bristol, BS1 1JQ',
     'price range': '£-££',
     'webpage': '',
     'opening times': 'Mon–Sat: 12:00 – 16:00 (Closed Sunday)'},
    {'id': 1,
     'name': 'Asado',
     'cuisine': 'Burgers',
     'address': '90 Colston Street, Bristol, BS1 5BB',
     'price range': '££-£££',
     'webpage': 'http://www.asadobristol.com/',
     'opening times': 'Sun: 09:00 – 23:00, Tue–Sat: 12:00 – 23:00 (Closed Monday)'},
    {'id': 2,
     'name': 'Beerd',
     'cuisine': 'Pizza',
     'address': '157-159 St Michaels Hill, Cotham, Bristol, BS2 8DB',
     'price range': '££-£££',
     'webpage': 'https://beerdbristol.com/',
     'opening times': 'Sun: 15:00 – 22:00, Mon–Thur: 16:00 – 22:00, Fri & Sat: 12:00 – 22:00'},
    {'id': 3,
     'name': 'Beirut Mezze',
     'cuisine': 'Lebanese / Halal',
     'address': '13a Small Street, Bristol, BS1 1DE',
     'price range': '££-£££',
     'webpage': 'http://www.beirutmezze.com/',
     'opening times': 'Sun: 17:30 – 22:45, Mon–Thur: 17:30 – 23:00, Fri & Sat: 17:00 – 23:00'},
    {'id': 4,
     'name': "Bertha's Pizza",
     'cuisine': 'Pizza',
     'address': 'The Old Gaol Stables, Cumberland Road, Bristol, BS1 6WW',
     'price range': '££-£££',
     'webpage': 'http://berthas.co.uk/bookings/?LMCL=i8_eeS',
     'opening times': 'Wed & Thurs: 17:00 – 21:00, Fri & Sat: 11:30 – 14:00 and 17:00 – 22:00, Sun: 11:30 – 16:00 (Closed Monday & Tuesday)'},
    {'id': 5,
     'name': 'Bomboloni',
     'cuisine': 'Italian',
     'address': '225 Gloucester Road, Bishopston, Bristol, BS7 8NR',
     'price range': '££-£££',
     'webpage': 'https://bomboloni.net/',
     'opening times': 'Tue–Sat: 10:00 – 22:00 (Closed Sunday and Monday)'},
    {'id': 6,
     'name': 'The Burger Joint',
     'cuisine': 'Burgers',
     'address': '83 Whiteladies Road, Clifton, Bristol, BS8 2NT & 240 North Street, Bedminster, Bristol, BS3 1JD',
     'price range': '£££-££££',
     'webpage': 'https://www.theburgerjoint.co.uk/',
     'opening times': 'Sun–Tue: 12:00 – 22:00, Wed & Thurs: 12:00 – 22:30, Fri & Sat: 12:00 – 23:00'},
    {'id': 7,
     'name': 'Carribean Wrap',
     'cuisine': 'Carribean',
     'address': 'St Nicholas Market, Bristol, BS1 1JQ',
     'price range': '£-££',
     'webpage': 'https://www.facebook.com/Caribbean-Wrap-Bristol-577537682267740/',
     'opening times': 'Mon–Sat: 12:00 – 17:00 (Closed Sunday)'},  
    {'id': 8,
     'name': 'Chilli Daddy',
     'cuisine': 'Street Food',
     'address': '45-47 Baldwin Street, Bristol, BS1 1RA',
     'price range': '£-££',
     'webpage': 'https://www.chillidaddy.com/',
     'opening times': 'Sun-Thur: 11:00 – 21:00, Fri & Sat: 11:00 – 22:00'}, 
    {'id': 9,
     'name': 'Eat A Pitta',
     'cuisine': 'Mediterranean / Vegetarian',
     'address': '1-3 Glass Arcade Street, Bristol, BS1 1LJ',
     'price range': '£-££',
     'webpage': 'https://www.eatapitta.co.uk/',
     'opening times': 'Sun: 11:00 – 17:30, Mon–Sat: 11:00 – 20:00'}, 
    {'id': 10,
     'name': "Edna's Kitchen",
     'cuisine': 'Cafe',
     'address': 'Castle Park, Wine Street, Bristol, BS1 2DN',
     'price range': '£-££',
     'webpage': 'www.ednas-kitchen.com',
     'opening times': 'Mon-Sun: 11:00 – 17:00'}, 
    {'id': 11,
     'name': 'Falafel King',
     'cuisine': 'Mediterranean / Vegetarian',
     'address': '6 Cotham Hill, Redland, Bristol, BS6 6LF',
     'price range': '£-££',
     'webpage': 'https://www.falafelkingbristol.com/',
     'opening times': 'Sun: 11:00 – 19:30, Mon–Sat: 10:30 – 22:30'}, 
    {'id': 12,
     'name': 'Fishminster',
     'cuisine': 'Fish & Chips',
     'address': '267 North Street, Bedminster, Bristol, BS3 1JN',
     'price range': '£-££',
     'webpage': 'https://fishminster.co.uk/',
     'opening times': 'Sun: 17:00 – 22:00, Mon–Wed: 11:30 – 14:00 and 17:00 – 22:30, Thu–Sat: 11:30 – 22:30'}, 
    {'id': 13,
     'name': 'Harbour and Browns',
     'cuisine': 'International',
     'address': 'Unit 13, Cargo 2, Museum Street Opposite the M Shed, Bristol, BS1 6ZA',
     'price range': '££-£££',
     'webpage': 'https://harbourandbrowns.com/',
     'opening times': 'Sun: 12:00 – 16:00, Tue & Wed: 18:00 – 23:00, Thur & Fri: 12:00 – 23:00, Sat: 10:00 – 23:00 (Closed Monday)'}, 
    {'id': 14,
     'name': 'Matina',
     'cuisine': 'Middle Eastern',
     'address': 'St Nicholas Market, Bristol, BS1 1JQ',
     'price range': '£-££',
     'webpage': 'https://www.facebook.com/Matina-Middle-Eastern-1610754745830638/',
     'opening times': 'Mon–Sat: 11:00 – 17:00 (Closed Sunday)'}, 
    {'id': 15,
     'name': 'Pickle Bristol',
     'cuisine': 'Cafe',
     'address': 'Underfall Yard, Hotwells, Bristol, BS1 6XG',
     'price range': '£-££',
     'webpage': 'https://en-gb.facebook.com/picklebristol/',
     'opening times': 'Tue–Fri: 09:00 – 17:00, Sat & Sun: 09:00 – 18:00 (Closed Monday)'}, 
    {'id': 16,
     'name': 'Pie Minister',
     'cuisine': 'British',
     'address': '7 Broad Quay, Bristol, BS1 4DA',
     'price range': '££-£££',
     'webpage': 'https://pieminister.co.uk/restaurants/broadquay/',
     'opening times': 'Sun: 12:00 – 21:00, Mon–Sat: 12:00 – 22:00'}, 
    {'id': 17,
     'name': 'Rice & Things',
     'cuisine': 'Carribean',
     'address': '120 Cheltenham Road, Bristol, BS6 5RW',
     'price range': '££-£££',
     'webpage': 'https://riceandthings.co.uk/',
     'opening times': 'Sun: 11:00 – 20:00, Mon-Fri: 12:00 – 22:00, Sat: 12:00 – 23:00'},
    {'id': 18,
     'name': 'Rollin Vietnamese',
     'cuisine': 'Vietnamese',
     'address': '23-25 The Arcade, Broadmead, Bristol, BS1 3JD',
     'price range': '£-££',
     'webpage': 'https://www.facebook.com/rollin.vietnamese/',
     'opening times': 'Mon–Sun: 10:00 – 19:00'}, 
    {'id': 19,
     'name': 'The Pickled Brisket',
     'cuisine': 'Street Food',
     'address': 'Cargo 2, Wapping Wharf, Bristol, BS1 6WE',
     'price range': '££-£££',
     'webpage': 'https://thepickledbrisket.co.uk/',
     'opening times': 'Tue & Wed: 12:00 – 15:00, Thurs: 12:00 – 16:00, Fri & Sat: 12:00 – 18:00, Sun: 12:00 – 16:00 (Closed Monday)'}, 
    {'id': 20,
     'name': 'The Real Greek',
     'cuisine': 'Greek',
     'address': '84a Glass House, Cabot Circus, Bristol, BS1 3BX',
     'price range': '££-£££',
     'webpage': 'https://www.therealgreek.com/restaurants/bristol/',
     'opening times': 'Sun: 12:00 – 20:00, Mon-Sat: 12:00 – 21:00'},  
    {'id': 21,
     'name': 'The Rose of Denmark',
     'cuisine': 'British',
     'address': '6 Dowry Place, Hotwells, Bristol, BS8 4QL',
     'price range': '££-£££',
     'webpage': 'https://www.facebook.com/roseofdenmarkbristol/',
     'opening times': 'Mon-Sun: 12:00 - 23:00'}, 
    {'id': 22,
     'name': 'The Woolly Cactus',
     'cuisine': 'Mexican',
     'address': 'The Keg Store, 1 Bath Street, Redcliffe, Bristol, BS1 6HL',
     'price range': '£-££',
     'webpage': 'www.thewoollycactus.co.uk',
     'opening times': 'Mon–Fri: 11:00 – 15:00 (Closed Saturday & Sunday)'},
    {'id': 23,
     'name': 'Tuk Tuck',
     'cuisine': 'Japanese / Asian / Korean',
     'address': '5 St Stephens Street, Bristol, BS1 1EE',
     'price range': '££-£££',
     'webpage': 'https://www.facebook.com/TukTuck-737841626257740/',
     'opening times': 'Sun: 15:00 – 22:00, Mon-Thur: 16:00 – 22:00, Fri & Sat: 12:00 – 22:00'}
]

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()


# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d

# @app.route('/', methods=['GET'])
# def home():
#     return "<h1>Bristol Fodder</h1><p>This site is a prototype API for places to eat in Bristol</p>"

# @app.route('/index', methods=['GET'])
# def index():
#     return "<h1>Index Page</h1><p>Reserved Index Page</p>"

# # A route to return all of the available entries in our catalog.
# @app.route('/api/v1/entries/places/all', methods=['GET'])
# def api_all():
#     conn = sqlite3.connect('places.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     all_places = cur.execute('SELECT * FROM places;').fetchall()
#     return jsonify(all_places)

# @app.errorhandler(404)
# def page_not_found(e):
#     return "<h1>404</h1><p>The entry could not be found.</p>", 404

# @app.route('/api/v1/entries/places', methods=['GET'])
# def api_filter():
#     query_parameters = request.args

#     id = query_parameters.get('id')
#     name = query_parameters.get('name')
#     cuisine = query_parameters.get('cuisine')
#     address = query_parameters.get('address')
#     price_range = query_parameters.get('price_range')
#     webpage = query_parameters.get('webpage')
#     opening_times = query_parameters.get('opening_times')


#     query = "SELECT * FROM places WHERE"
#     to_filter = []

#     if id:
#         query += ' id=? AND'
#         to_filter.append(id)
#     if name:
#         query += ' name=? AND'
#         to_filter.append(name)
#     if cuisine:
#         query += ' cuisine=? AND'
#         to.filter.append(cuisine)
#     if address:
#         query += ' address=? AND'
#         to_filter.append(address)
#     if price_range:
#         query += ' price_range=? AND'
#         to_filter.append(price_range)
#     if webpage:
#         query += ' webpage=? AND'
#         to_filter.append(webpage)
#     if opening_times:
#         query += ' opening_times=? AND'
#         to_filter.append(opening_times)V
#     if not (id or name or cuisine or address or price_range or webpage or opening_times):
#         return page_not_found(404)

#     query = query[:-4] + ';'

#     conn = sqlite3.connect('places.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()

#     results = cur.execute(query, to_filter).fetchall()

#     return jsonify(results)

# app.run()


conn = psycopg2.connect(dsn)
cur = conn.cursor()
cur.execute(sql, (value1,value2))
