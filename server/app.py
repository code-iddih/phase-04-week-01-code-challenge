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
    # Query all heroes from the database
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






























if __name__ == '__main__':
    app.run(port=5555, debug=True)