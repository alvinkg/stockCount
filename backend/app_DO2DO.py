import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pathlib import Path

from flask import Flask, request, json, jsonify
# , render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, Computed, func, case
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies
from flask_cors import CORS

import psycopg2

from models_DO import db, Name, Product, Event, Cart, Wallet, format_event, format_name

# Use this if we don't connect via SQLAlchemy
#print(dotenv_path)
# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
# dotenv_path = Path('../.env-remote')
load_dotenv('./.env-localDO') # can use the var dotenv_path, # take environment variables from .env.
url = os.getenv("SQLALCHEMY_DATABASE_URI")
#url=psycopg2.connect('postgresql://alvin:alvin@localhost/alvin')

print('url:', url)
#connection = psycopg2.connect(url)

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))

# import env var from settings.py, in turn from .env
# app.config.from_pyfile('/Users/alvinlim/Documents/Code/baby-tracker/settings.py')
# app.config.get('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_DATABASE_URI']= os.getenv("SQLALCHEMY_DATABASE_URI")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# instantiate cors
# CORS(app)

CORS(app, supports_credentials=True)
 
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = "topsecretkey"
# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://alvin:alvin@localhost/alvin'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# create bcrypt obj
bcrypt = Bcrypt(app)

# initialize the app with the extension
db.init_app(app)
# After all models and tables are defined, call SQLAlchemy.create_all() to create the table schema in the database. 
with app.app_context():
    db.create_all()

# config JWT    
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# initializing a JWTManager with flask app before using
jwt =JWTManager(app)

# Takes entry and passes it jsonified to the FE
def format_cart(cart):
    return {
        "cartId": cart.id,
        "created_at": cart.created_at
    }

@app.route('/cart', methods=['POST'])
def create_cart():
    #1 Grab the params from the request & assign to var
    title = request.json['title']
    price = request.json['price']
    
    # instan Cart? obj
    cart = Cart(title,price)
    db.session.add(cart)
    db.session.commit()
    return format_cart(cart)

@app.route('/carts', methods=['GET'])
def get_carts():
    carts = Cart.query.order_by(Cart.created_at.asc()).all() # Cart.id.asc()
    cart_list = []
    for cart in carts:
        cart_list.append(format_cart(cart))
    return {'cart': cart_list}

#####################################

# Takes entry and passes it jsonified to the FE
def format_product(product):
    return {
        "title": product.title,
        "id": product.id,
        "price": product.price,
        "image": product.image,
        "sid": product.sid,
        "created_at": product.created_at
    }

@app.route('/product', methods=['POST'])
def create_product():
    #1 Grab the params from the request & assign to var
    title = request.json['title']
    price = request.json['price']
    image = request.json['image']
    sid = request.json['sid']
    
    # instan Product? obj
    product = Product(title,price,image,sid)
    db.session.add(product)
    db.session.commit()
    return format_product(product)

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    # #1 Grab the params from the request & assign to vars
    # description = request.json['description']
    # #2 inst event obj from db
    # event = Event.query.get(id)
    # #3 update the event obj
    # event.description = description
    # #4 commit changes
    # db.session.commit()
    # #5 return serialized/formatted obj
    # return  {'event': format_event(event)}

    # Option 2
    #1 Grab the params from the request & assign to vars
    title = request.json['title']
    price = request.json['price']
    image = request.json['image']
    #2 gets obj as a list
    product = Product.query.filter_by(id=id)
    #3 update the event obj with vars
    product.update(dict(title=title,price=price,image=image,created_at=datetime.utcnow()))
     # #4 commit changes
    db.session.commit()
    #5 return serialized/formatted obj
    return {'product': format_product(product.one())}

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.order_by(Product.created_at.asc()).all() # Cart.id.asc()
    product_list = []
    for product in products:
        product_list.append(format_product(product))
    return {'products': product_list}

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.filter_by(id=id).one()
    formatted_product = format_product(product)
    return {'product': formatted_product}

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.filter_by(id=id).one()
    db.session.delete(product)
    db.session.commit()
    return f"Product {id} has been deleted successfully."
    # formatted_event = format_event(event)
    # return {'event': formatted_event}
   
#####################################

@app.route('/')
def hello():
    # return render_template('index.html')
    # access_token = create_access_token()
    # return jsonify(message='password exists.')
    response = jsonify(message='success') #,access_token=access_token
    return response, 201

# create an event
@app.route('/events', methods=['POST'])
def create_event():
    #1 Grab the params from the request & assign to var
    description = request.json['description']
    quantity = request.json['quantity']
    reorder = request.json['reorder']
    safety = request.json['safety']
    # instan Event obj
    # event = Event(description, quantity)
    event = Event(description, quantity, reorder, safety)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

# get all events
@app.route('/events', methods=['GET'])
def get_events():
    # order by created_at / id
    events = Event.query.order_by(Event.id.asc()).all()
    # events = Event.query.order_by(Event.created_at.desc()).all()

    # create empty event list
    event_list = []
    for event in events:
        # append each event to the list
        event_list.append(format_event(event))
    return {'events': event_list}

# get single event
@app.route('/events/<id>', methods=['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).one()
    formatted_event = format_event(event)
    return {'event': formatted_event}

# delete an event by id
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return f"Event {id} has been deleted successfully."

# edit an event with id  
@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    #1 Grab the event by id
    event = Event.query.filter_by(id=id)
    #2 gets description
    description = request.json['description']
    quantity = request.json['quantity']
    reorder = request.json['reorder']
    safety = request.json['safety']
    #3 update the event obj with description 
    event.update(dict(description=description, quantity=quantity, reorder=reorder, safety=safety, created_at=datetime.utcnow()))
     # #4 commit changes
    db.session.commit()
    #5 return serialized/formatted obj
    return {'event': format_event(event.one())}



def format_wallet(wallet):
    return {
        "product": wallet.product,
        "topup": wallet.topup,
        "price": wallet.price,
        "id": wallet.id,
        "date_time": wallet.date_time,
        "created_at": wallet.created_at
    }

@app.route('/wallet', methods=['POST'])
# @jwt_required() # only available with token
def create_topup():
    #1 Grab the params from the request & assign to var
    # TODO: how to make the below flexible if data is missing
    topup = request.json['topup']
    price = request.json['price']
    balance = request.json['balance']
    product = request.json['product']
    date_time = request.json['datetime']
    
    # instan Wallet? obj
    wallet = Wallet(topup,price,balance,product,date_time)
    db.session.add(wallet)
    db.session.commit()
    return format_wallet(wallet)

#####################################

# get all names
@app.route('/names', methods=['GET'])
def get_names():
    # order by created_at / id
    names = Name.query.order_by(Name.id.asc()).all()
    # events = Event.query.order_by(Event.created_at.desc()).all()

    # create empty event list
    name_list = []
    for name in names:
        # append each event to the list
        name_list.append(format_name(name))
    return {'names': name_list}

# get single name
@app.route('/names/<id>', methods=['GET'])
def get_name(id):
    name = Name.query.filter_by(id=id).one()
    formatted_name = format_name(name)
    return {'name': formatted_name}

@app.route('/logintoken', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = Name.query.filter_by(email=email).first()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')

    print("password:", password)
    print("hashed_password:", hashed_password)
    if user is None:
        return jsonify({"error": "Wrong email or password"}), 401
    else:
        print("user.password:", user.password)
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    access_token = create_access_token(identity=email)
    response = jsonify({
        "msg": "login successful",
        "access_token": access_token
    })
    set_access_cookies(response, access_token)
    
    return {
        "msg": "Success",
        "email": email,
        "password": password,
        "access_token": access_token
    }
    
# mtd to create a name in Name table
@app.route("/signup", methods=["POST"])
def signup():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]
    name_exists = Name.query.filter_by(email=email).first() is not None

    if name_exists:
        return jsonify({"error": "Name with this email already exists."}), 409
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
    print("hashed password:", hashed_password)
    new_name = Name(email=email, password=hashed_password, name=name, about="what about me?")
    print("new user password:", new_name.password)
    db.session.add(new_name)
    db.session.commit()
    
    return jsonify({
        "id": new_name.id,
        "email": email,
        "password": new_name.password
    })

# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens.html
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT.  Just return the original response
        return response

@app.route("/profile/<getemail>")
@jwt_required() # only available with token
def my_profile(getemail):
    print("getemail:", getemail)
    
    if not getemail: # if it doesn't have value / exist
        # this does not get to work
        return jsonify({"error": "Unauthorized Access"}), 401
    
    user = Name.query.filter_by(email=getemail).first()
    print("user:", user)
    
    if user == None:
        return "No such user"
    else:
        response_body = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "about": user.about
        }
        
        return response_body

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

#####################################

# with app.app_context():
# #     from app import db
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
