from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates  # Import the validates function

# Defining naming convention for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initializing SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)

# Hero Model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules = ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # Relationship with HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # Many-to-many relationship with Power
    powers = db.relationship('Power', secondary='hero_powers', back_populates='heroes', overlaps='hero_powers')

    def __repr__(self):
        return f'<Hero {self.id}: {self.name} aka {self.super_name}>'

# Power Model
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    serialize_rules = ('-hero_powers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # Relationship with HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    # Many-to-many relationship with Hero
    heroes = db.relationship('Hero', secondary='hero_powers', back_populates='powers', overlaps='hero_powers')

    def __repr__(self):
        return f'<Power {self.id}: {self.name} - {self.description}>'

# HeroPower Model (association table)
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # Foreign Keys with cascade deletes
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'))

    # Relationships with overlaps parameter
    hero = db.relationship('Hero', back_populates='hero_powers', overlaps='powers')
    power = db.relationship('Power', back_populates='hero_powers', overlaps='heroes')

    def __repr__(self):
        return f'<HeroPower Strength {self.strength}>'

    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError(f"strength must be one of the following values: {', '.join(valid_strengths)}")
        return value

    @validates('hero_id', 'power_id')
    def validate_ids(self, key, value):
        if value is None:
            raise ValueError(f"{key} must not be null")
        return value
    
    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("description must be present")
        if len(value) < 20:
            raise ValueError("description must be at least 20 characters long")
        return value
