from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flight_admin:6kKVm7C2PHtVtgGT@esd-g7t6-rds.cs2kfkrucphj.ap-southeast-1.rds.amazonaws.com:3306/flight_pricing'

# set dbURL=mysql+mysqlconnector://root@localhost:3306/book

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)
CORS(app)


class Baggage(db.Model):
    __tablename__ = 'baggage'

    baggage_id = db.Column(db.Integer, primary_key=True)
    baggage_desc = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, baggage_id, baggage_desc, price):
        self.baggage_id = baggage_id
        self.baggage_desc = baggage_desc
        self.price = price

    def json(self):
        return {
            "baggage_id": self.baggage_id,
            "baggage_desc": self.baggage_desc,
            "price": self.price
        }

class Class_type(db.Model):
    __tablename__ = 'class_type'

    class_name = db.Column(db.String(20), primary_key=True)
    percentage = db.Column(db.Float, nullable=False)

    def __init__(self, class_name, price):
        self.class_name = class_name
        self.percentage = percentage

    def json(self):
        return {
            "class_name": self.class_name,
            "percentage": self.percentage
        }

class Meal(db.Model):
    __tablename__ = 'meal'

    meal_id = db.Column(db.Integer, primary_key=True)
    meal_desc = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, meal_id, meal_desc, price):
        self.meal_id = meal_id
        self.meal_desc = meal_desc
        self.price = price

    def json(self):
        return {
            "meal_id": self.meal_id,
            "meal_desc": self.meal_desc,
            "price": self.price
        }


@app.route("/pricing")
def get_all():
    return jsonify({
        "baggages": [baggage.json() for baggage in Baggage.query.all()],
        "classes": [class_type.json() for class_type in Class_type.query.all()],
        "meals": [meal.json() for meal in Meal.query.all()]
        })

@app.route("/pricing/baggage/<int:baggage_id>")
def get_baggage_price(baggage_id):
    baggage = Baggage.query.filter_by(baggage_id=baggage_id).first()
    if baggage:
        return jsonify(baggage.json())
    return jsonify({"message": "Couldn't find baggage"}), 404

@app.route("/pricing/meal/<int:meal_id>")
def get_meal_price(meal_id):
    meal = Meal.query.filter_by(meal_id=meal_id).first()
    if meal:
        return jsonify(meal.json())
    return jsonify({"message": "Couldn't find meal"}), 404

@app.route("/pricing/class/<string:class_name>")
def get_class_price(class_name):
    class_name = Class_type.query.filter_by(class_name=class_name).first()
    if class_name:
        return jsonify(class_name.json())
    return jsonify({"message": "Couldn't find class type"}), 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)