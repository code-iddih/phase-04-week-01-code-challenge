#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
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

# Getting Powers
@app.route('/powers', methods=['GET'])
def get_powers():
    # Querying all powers from the database
    powers = Power.query.all()
    
    # Preparing the response data
    response_data = []
    for power in powers:
        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        response_data.append(power_data)
    
    return jsonify(response_data), 200

# Getting Powers By ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    # Querying the database for the power with the specified id
    power = Power.query.get(id)

    if power:
        # Preparing the response data for the existing power
        response_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return jsonify(response_data), 200
    else:
        # If the power does not exist, return an error message
        return jsonify({"error": "Power not found"}), 404
    
# Updating Power
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    # Fetching the power by ID
    power = Power.query.get(id)
    
    # If power does not exist, return error
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    # Getting the JSON data from the request
    data = request.get_json()

    # Validaing the description field
    if 'description' not in data:
        return jsonify({"errors": ["description must not be empty"]}), 400

    description = data['description']

    # Checking if description is empty
    if not description.strip():
        return jsonify({"errors": ["description must not be empty"]}), 400

    # Checking if description length is at least 20 characters
    if len(description) < 20:
        return jsonify({"errors": ["description must be at least 20 characters long"]}), 400

    # Updaing the power's description
    power.description = description
    
    # Committing the changes to the database
    db.session.commit()
    
    # Returning the updated power details
    return jsonify({
        "description": power.description,
        "id": power.id,
        "name": power.name
    }), 200































if __name__ == '__main__':
    app.run(port=5555, debug=True)