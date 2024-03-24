from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', lazy=True)
    pizzas = association_proxy('restaurant_pizzas', 'pizza')
    # add serialization rules
    
    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', lazy=True)
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    # add serialization rules

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)    
    # add serialization rules
    serialize_rules=('-pizza', '-restaurant',)

    # add validation
    @validates('price', include_backrefs=False)
    def validate_price(self, key, price):
        if 0< price <30:
            pass
        else:
            raise ValueError('price must be  0 < price < 30 ')
        return price

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'

