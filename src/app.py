import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, FavoriteCharacter, FavoritePlanet

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id', 1)
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    favorite_characters = FavoriteCharacter.query.filter_by(user_id=user_id).all()
    characters = [
        {
            "type": "character",
            "id": fav.character_id,
            "name": fav.character.name
        }
        for fav in favorite_characters
    ]
    
    favorite_planets = FavoritePlanet.query.filter_by(user_id=user_id).all()
    planets = [
        {
            "type": "planet",
            "id": fav.planet_id,
            "name": fav.planet.name
        }
        for fav in favorite_planets
    ]
    
    return jsonify({
        "user_id": user_id,
        "username": user.username,
        "favorites": {
            "characters": characters,
            "planets": planets
        }
    }), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id', 1)
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    
    existing_favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"message": "Planet already in favorites"}), 200
    
    new_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Planet added to favorites"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id', 1)
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    
    existing_favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if existing_favorite:
        return jsonify({"message": "Character already in favorites"}), 200
    
    new_favorite = FavoriteCharacter(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Character added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id', 1)
    
    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite planet not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet deleted successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.json.get('user_id', 1)
    
    favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite character not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite character deleted successfully"}), 200

@app.route('/people', methods=['POST'])
def create_person():
    data = request.json
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    
    new_person = Character(
        name=data.get('name'),
        height=data.get('height'),
        mass=data.get('mass'),
        hair_color=data.get('hair_color'),
        eye_color=data.get('eye_color'),
        birth_year=data.get('birth_year'),
        gender=data.get('gender')
    )
    
    db.session.add(new_person)
    db.session.commit()
    
    return jsonify({"message": "Character created", "character": new_person.serialize()}), 201

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    
    data = request.json
    for field in ['name', 'height', 'mass', 'hair_color', 'eye_color', 'birth_year', 'gender']:
        if field in data:
            setattr(person, field, data[field])
    
    db.session.commit()
    return jsonify({"message": "Character updated", "character": person.serialize()}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Character deleted"}), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    
    new_planet = Planet(
        name=data.get('name'),
        diameter=data.get('diameter'),
        climate=data.get('climate'),
        population=data.get('population'),
        terrain=data.get('terrain')
    )
    
    db.session.add(new_planet)
    db.session.commit()
    
    return jsonify({"message": "Planet created", "planet": new_planet.serialize()}), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    
    data = request.json
    for field in ['name', 'diameter', 'climate', 'population', 'terrain']:
        if field in data:
            setattr(planet, field, data[field])
    
    db.session.commit()
    return jsonify({"message": "Planet updated", "planet": planet.serialize()}), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": "Planet deleted"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
