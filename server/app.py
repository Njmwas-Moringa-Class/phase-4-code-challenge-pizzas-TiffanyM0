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
    restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id=id).all()
    if restaurants: 
        if request.method == 'GET':

            restaurant_dict = {
                'address': restaurants.address,
                'id' : restaurants.id,
                'name' : restaurants.name,
                'restaurant_pizzas' : []
            }
            for restaurant in restaurant_pizzas:
                restaurant_pizzas_dict = {
                    'id': restaurant.id, 
                    "pizza": [],
                    "pizza_id": restaurant.pizza_id,
                    "price": restaurant.price,
                    "restaurant_id": restaurant.restaurant_id
                }
                restaurant_dict['restaurant_pizzas'].append(restaurant_pizzas_dict)

                pizza_restaurant = restaurant_pizzas_dict['pizza_id']

                pizzas = Pizza.query.filter_by(id=pizza_restaurant).all()

                for restaurant_pizzas in pizzas:
                    pizza_dict = {
                        'id' : restaurant_pizzas.id,
                        'name': restaurant_pizzas.name,
                        'ingredients' : restaurants.pizza.ingredients,
                    }
                    restaurant_pizzas_dict['pizza'].append(pizza_dict)
                restaurant_dict['restaurant_pizzas'].append(restaurant_pizzas_dict)

            response= make_response(
                jsonify(restaurant_dict), 
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
        restaurants = Restaurant.query.all()
        restaurant_pizzas = []

        for res in RestaurantPizza.query.all():
            res_dict = {
                'id': res.id, 
                "pizza": [],
                "pizza_id": res.pizza_id,
                "price": res.price,
                "restaurant": [],
                "restaurant_id": res.restaurant_id
            }
        for restaurant in restaurants:
            restaurant_dict = {
                'id' : restaurant.id,
                'name': restaurant.name,
                'address' : restaurant.address,
            }
            for restaurant_pizza in restaurant.pizza:
                pizza_dict = {
                    'id' : restaurant_pizza.pizza.id,
                    'name': restaurant_pizza.pizza.name,
                    'ingredients' : restaurant_pizza.pizza.ingredients
                }
            res_dict['pizza'].append(pizza_dict)
        res_dict['restaurant'].append(restaurant_dict)
        restaurant_pizzas.append(res_dict)

        response = make_response(
            jsonify(restaurant_pizzas), 
            201
        )

        return response
    
    elif request.method == 'POST':

        price = request.form.get('price')

        if (price in range(1, 30)):
            new_restaurant_pizzas = RestaurantPizza(
                price=price,
                pizza_id=request.form.get('pizza_id'),
                restaurant_id=request.form.get('restaurant_id')
            )

            db.session.add(new_restaurant_pizzas)
            db.session.commit()
            new_restaurant_pizzas_dict = {
                'price' : new_restaurant_pizzas.price,
                'pizza_id' : new_restaurant_pizzas.pizza_id,
                'restaurant_id' : new_restaurant_pizzas.restaurant_id
            }

            response = make_response(
                jsonify(new_restaurant_pizzas_dict), 
                201
            )
            return response
        
        else: 
            return make_response(jsonify({
                "errors": ["validation errors"]
            }), 400)
            




if __name__ == '__main__':
    app.run(port=5555, debug=True)
