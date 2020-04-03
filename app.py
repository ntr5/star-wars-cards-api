from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import cloudinary as Cloud

import os

app = Flask(__name__)
heroku = Heroku(app)
env = Env()
env.read_env()
CORS(app)
DATABASE_URL = env('DATABASE_URL')

Cloud.config.update = ({
    # 'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'cloud_name':"dtksvhogu",
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(1500))
    image_url = db.Column(db.String(500))
    public_id = db.Column(db.String(500))
    # offer = db.Column(db.Numeric(10, 2))
    # username = db.Column(db.String(100), nullable=True)
    # seller_id = db.Column(db.Integer)

    # def __init__(self, name, quantity, price, offer, image_url, seller_id):
    # def __init__(self, name, quantity, price, offer, description, image_url, username):
    def __init__(self, name, quantity, price, description, image_url, public_id):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.description = description
        self.image_url = image_url
        self.public_id = public_id
        # self.offer = offer
        # self.seller_id = seller_id
        # self.username = username


class CardSchema(ma.Schema):
    class Meta:
        # fields = ("id", "name", "quantity", "price", "offer", "image_url", "seller_id")
        # fields = ("id", "name", "quantity", "price", "offer", "description", "image_url", "username")
        # fields = ("id", "name", "quantity", "price", "description", "image_url", "username")
        fields = ("id", "name", "quantity", "price", "description", "image_url", "public_id")


card_schema = CardSchema()
cards_schema = CardSchema(many=True)


@app.route("/")
def greeting():
    return "<h1>Card Seller API<h1>"


#POST
@app.route("/add-card", methods=["POST"])
def add_card():
    name = request.json["name"]
    quantity = request.json["quantity"]
    price = request.json["price"]
    description = request.json["description"]
    image_url = request.json["image_url"]
    public_id = request.json["public_id"]
    # offer = request.json["offer"]
    # username = request.json["username"]
    # user_id = request.json["user_id"]

    # new_card = Card(name, quantity, price, offer, image_url, user_id)
    # new_card = Card(name, quantity, price, offer, description, image_url, username)
    # new_card = Card(name, quantity, price, description, image_url, username)
    new_card = Card(name, quantity, price, description, image_url, public_id)

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


#PUT update a card
@app.route("/card/<id>", methods=["PUT"])
def update_card(id):
    card = Card.query.get(id)

    name = request.json['name']
    quantity = request.json['quantity']
    price = request.json['price']
    description = request.json['description']
    image_url = request.json['image_url']
    public_id = request.json['public_id']
    # offer = request.json['offer']
    # username = request.json['username']
    # user_id = request.json['user_id']

    card.name = name
    card.quantity = quantity
    card.price = price
    card.description = description
    card.image_url = image_url
    card.public_id = public_id
    # card.offer = offer
    # card.username = username

    db.session.commit()
    return card_schema.jsonify(card)


#DELETE a card
@app.route("/card/<id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)

    db.session.delete(card)
    db.session.commit()
    Cloud.api.delete_resources([card.public_id])

    return "CARD WAS SUCCESSFULLY DELETED"


if __name__ == "__main__":
    app.debug = True
    app.run()