#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def get_restaurants():

    restaurants = []

    for restaurant in Restaurant.query.all():
        restaurants_dict= {
            "address" : restaurant.address,
            "id" : restaurant.id,
            "name" : restaurant.name,
        }
        restaurants.append(restaurants_dict)
    
    response = make_response(
        jsonify(restaurants)
    )
    return response

@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurants = Restaurant.query.filter_by(id=id).first()
    if restaurants: 
        if request.method == 'GET':
            restaurant_serialized = restaurants.to_dict()
            response= make_response(
                jsonify(restaurant_serialized), 
                200
            )
            return response
        
        elif request.method == 'DELETE':
            db.session.delete(restaurants)
            db.session.commit()
            response_body = {
                'deleted' : True
            }
            response = make_response(jsonify(response_body), 204)
            return response
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/pizzas')
def get_pizzas():
    pizzas = []
    for item in Pizza.query.all():
        pizzas_dict = {
            'id' : item.id,
            'ingredients' : item.ingredients,
            'name' : item.name
        }
        pizzas.append(pizzas_dict)
    response = make_response(
        jsonify(pizzas), 
        200
    )

    return response

@app.route('/restaurant_pizzas', methods = ['GET', 'POST'])
def get_restaurant_pizzas():

    if request.method == 'GET':
        restaurant_pizzas = []
        for pizza in RestaurantPizza.query.all():
            restaurant_pizzas_dict = {
                'id' : pizza.id,
                'price': pizza.price,
                'pizza_id' : pizza.price_id,
                'restaurant_id' : pizza.restaurant_id
            }
            restaurant_pizzas.append(restaurant_pizzas_dict)

        response = make_response(
            jsonify(restaurant_pizzas), 
            200
        )

        return response
    
    elif request.method == 'POST':

        new_restaurant_pizzas = RestaurantPizza(
            price=request.form.get('price'),
            pizza_id=request.form.get('pizza_id'),
            restaurant_id=request.form.get('restaurant_id')
        )

        db.session.add(new_restaurant_pizzas)
        db.session.commit()

        response = make_response(
            jsonify(new_restaurant_pizzas.to_dict()), 
            201
        )

        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
