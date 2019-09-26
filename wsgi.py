# wsgi.py
import os
import logging
#logging.warn(os.environ["DUMMY"])

from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/api/v1/products/<int:id>', methods=["GET"])
def get_product(id):

    product = db.query(Product).get(id)
    if product != None:
        return jsonify(product)
    return '', 404

@app.route('/api/v1/products/<int:id>', methods=["DELETE"])
def delete_product(id):
    for product in PRODUCTS:
        if product["id"] == id :
            print('delete')
            PRODUCTS.remove(product)
            return '', 204
    return '', 404

@app.route('/api/v1/products/', methods=["POST"])
def add_products():
    PRODUCTS.append({"id": 4 ,"name" : "Here"})
    return "", 201
