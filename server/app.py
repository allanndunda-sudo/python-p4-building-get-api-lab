#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []

    for bakery in Bakery.query.all():
        bakeries.append({
            "id": bakery.id,
            "name": bakery.name
        })

    return jsonify(bakeries), 200
    return ''

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    return jsonify([
        {
            "id": b.id,
            "name": b.name,
            "created_at": b.created_at.isoformat()
        } 
        for b in Bakery.query.all()
    ]), 200


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404

    return jsonify({
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at.isoformat() if bakery.created_at else None
    }), 200
    return ''

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    result = [
        {
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "created_at": bg.created_at.isoformat() 
        }
        for bg in baked_goods
    ]

    return jsonify(result), 200
    return ''

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()

    return jsonify({
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        "created_at": bg.created_at.isoformat() if bg.created_at else None
    }), 200
    return ''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
