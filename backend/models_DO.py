import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4
from flask import Flask, request, json, jsonify
# , render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from sqlalchemy import String, Computed, func, case
from sqlalchemy import create_engine, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database

import psycopg2

db = SQLAlchemy()

engine = create_engine('postgresql://alvin:alvin@localhost/alvin')
if not database_exists(engine.url):
    create_database(engine.url)
    print("engine url:", engine.url)
print(database_exists(engine.url))

def get_uuid():
    return uuid4().hex

class Name(db.Model):
    # note the creation of a unique id with uuid
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid) #
    name = db.Column(db.String(150), unique=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.Text, nullable=False)
    about = db.Column(db.Text, nullable=False)

def format_name(name):
    return {
        "id": name.id,
        "name": name.name,
        "email": name.email,
        # "password": name.password,
        "about": name.about,
    }

##################################### 
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sid = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    carts = db.relationship('Cart',backref='product')
    # products = db.relationship('Cart',backref='product')
    
    # used for debugging to give string representation of obj
    def __repr__(self):
        return f'Product: {self.title}'
    
    def __init__(self, title, price, image, sid): #
        self.title = title
        self.price = price
        self.image = image
        self.sid = sid

#####################################
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=True)
    reorder = db.Column(db.Integer, nullable=True)
    safety = db.Column(db.Integer, nullable=True)
    buy = db.Column(db.Integer, Computed(case((safety >= quantity, reorder - quantity), else_=0)))
    description = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'Event: {self.description}'
    
    def __init__(self, description, quantity, reorder, safety):
        self.description = description
        self.quantity = quantity
        self.reorder = reorder
        self.safety = safety
 
def format_event(event):
    return {
        "description": event.description,
        "quantity": event.quantity,
        "reorder": event.reorder,
        "safety": event.safety,
        "buy": event.buy,
        "id": event.id,
        "created_at": event.created_at
    }

#####################################
    
class Cart(db.Model):
    cartId = db.Column(db.Integer, primary_key=True)
    # productId = db.Column(db.Integer,db.ForeignKey('product.title'))
    purchased = db.Column(db.Boolean)
    id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    # product_name = db.Column(db.String(100), db.ForeignKey('product.id'))
    
    # used for debugging to give string representation of obj
    def __repr__(self):
        return f'Cart: {self.cartId, self.purchased}'
    
    def __init__(self, sessionID, purchased): #
        self.cartID = sessionID
        self.purchased = purchased

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    product = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)  
    topup = db.Column(db.Float, nullable=True)
    balance = db.Column(db.Float, nullable=True)
    date_time = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # used for debugging to give string representation of obj
    def __repr__(self):
        return f'Wallet: {self.topup}'
    
    def __init__(self, topup, price, balance,product,datetime): #
        self.topup = topup
        self.price = price
        self.balance = balance
        self.product = product
        self.date_time = datetime
