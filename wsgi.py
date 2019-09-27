# wsgi.py
import os
import logging
#logging.warn(os.environ["DUMMY"])

from flask import Flask, render_template

#from flask import Flask, jsonify, request
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/')
def home():
    products = db.session.query(Product).all()

    return render_template('home.html', products=products)

@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    print (products, flush=True)
    return products_schema.jsonify(products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)
    print (id, flush=True)
    print (product, flush=True)
    if product != None:
        return product_schema.jsonify(product), 200
    return '', 404

@app.route('/api/v1/products/<int:id>', methods=["DELETE"])
def delete_product(id):
    product = db.session.query(Product).get(id)
    print (id, flush=True)
    print (product, flush=True)
    if product != None:
        db.session.delete(product)
        db.session.commit()
        return '', 204
    return '', 404

@app.route('/api/v1/products', methods=["POST"])
def add_products():

    product_name = request.form.get('name')
    print(product_name, flush=True)
    product_description = request.form.get('description')
    print(product_description, flush=True)
    product = Product(name=product_name,description=product_description)
    print(product, flush=True)
    db.session.add(product)
    db.session.commit()
    return "", 201

@app.route('/api/v1/products/<int:id>', methods=["PATCH"])
def update_products(id):
    product = db.session.query(Product).get(id)
    print (id, flush=True)
    print (product, flush=True)
    product.name = request.form.get('name')
    print(product, flush=True)
    db.session.commit()
    return "", 201
