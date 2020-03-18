from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import os
# import psycopg2

app = Flask(__name__)
heroku = Heroku(app)
env = Env()
env.read_env()
# DATABASE_URL = env('DATABASE_URL')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")


# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# conn = psycopg2.connect("dbname=postgres user=deployer")

# app.config['SQLALCHEMY_DATABASE_URI'] - MONGO_URL
# MONGO_URL = os.environ.get('MONGO_URL')
# if not MONGO_URL:
#     MONGO_URL = "mongodb://heroku_kmg4vfxb:t4db3q35fvk5uhmm5rjjetudt7@ds033145.mlab.com:33145/heroku_kmg4vfxb";

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    offer = db.Column(db.Numeric(10, 2))
    # price = db.Column(db.String(20))
    # offer = db.Column(db.String(20))
    image_url = db.Column(db.String(500))
    seller_id = db.Column(db.Integer)

    def __init__(self, name, quantity, price, offer, image_url, seller_id):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.offer = offer
        self.image_url = image_url
        self.seller_id = seller_id


class CardSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "quantity", "price", "offer", "image_url", "seller_id")


card_schema = CardSchema()
cards_schema = CardSchema(many=True)


@app.route("/")
def greeting():
    return "<h1>Card Seller API<h1>"


#POST
# @app.route("/post-card", methods=["POST"])
@app.route("/add-card", methods=["POST"])
def add_card():
    name = request.json["name"]
    quantity = request.json["quantity"]
    price = request.json["price"]
    offer = request.json["offer"]
    image_url = request.json["image_url"]
    seller_id = request.json["seller_id"]

    new_card = Card(name, quantity, price, offer, image_url, seller_id)

    db.session.add(new_card)
    db.session.commit()

    return jsonify("Card POSTED")


#GET all cards
@app.route("/cards", methods=["GET"])
def get_cards():
    all_cards = Card.query.all()
    result = cards_schema.dump(all_cards)

    return jsonify(result)


#GET one card
@app.route("/card/<id>", methods=["GET"])
def get_card(id):
    card = Card.query.get(id)

    return card_schema.jsonify(card)


#PUT
@app.route("/card/<id>", methods=["PUT"])
def update_card(id):
    card = Card.query.get(id)
    name = request.json['name']
    quantity = request.json['quantity']
    price = request.json['price']
    offer = request.json['offer']
    image_url = request.json['image_url']
    seller_id = request.json['seller_id']

    card.name = name
    card.quantity = quantity
    card.price = price
    card.offer = offer
    card.image_url = image_url
    card.seller_id = seller_id

    db.session.commit()
    return card_schema.jsonify(card)


#DELETE a card
@app.route("/card/<id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)

    db.session.delete(card)
    db.session.commit()

    return "CARD WAS SUCCESSFULLY DELETED"


if __name__ == "__main__":
    app.debug = True
    app.run()