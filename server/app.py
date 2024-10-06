#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower  

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  

migrate = Migrate(app, db)

db.init_app(app)

# Home Page
@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the Superhero API! Use /heroes to get a list of superheroes.'


# Getting Heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    # Querying all heroes from the database
    heroes = Hero.query.all()
    
    # Serializing the heroes
    hero_list = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        for hero in heroes
    ]
    
    return jsonify(hero_list)

# Getting heroes by ID and populating relevant details
@app.route('/heroes/<int:id>', methods=['GET'])
def fetch_hero(id):
    # Fetching the hero by ID along with their associated powers
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    response_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": []
    }

    for hero_power in hero.hero_powers:
        power = hero_power.power
        hero_power_data = {
            "hero_id": hero.id,
            "id": hero_power.id,
            "power_id": hero_power.power_id,
            "strength": hero_power.strength,
            "power": {
                "description": power.description,
                "id": power.id,
                "name": power.name
            }
        }
        response_data["hero_powers"].append(hero_power_data)

    return jsonify(response_data), 200





























if __name__ == '__main__':
    app.run(port=5555, debug=True)