from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="user", cascade="all, delete-orphan")
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "subscription_date": self.subscription_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Planet(db.Model):
    __tablename__ = 'planets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(20), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(20), nullable=True)
    diameter: Mapped[str] = mapped_column(String(20), nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    surface_water: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    characters: Mapped[list["Character"]] = relationship("Character", back_populates="homeworld")
    species: Mapped[list["Species"]] = relationship("Species", back_populates="homeworld")
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Species(db.Model):
    __tablename__ = 'species'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=True)
    designation: Mapped[str] = mapped_column(String(50), nullable=True)
    average_height: Mapped[str] = mapped_column(String(20), nullable=True)
    skin_colors: Mapped[str] = mapped_column(String(100), nullable=True)
    hair_colors: Mapped[str] = mapped_column(String(100), nullable=True)
    eye_colors: Mapped[str] = mapped_column(String(100), nullable=True)
    average_lifespan: Mapped[str] = mapped_column(String(20), nullable=True)
    language: Mapped[str] = mapped_column(String(100), nullable=True)
    homeworld_id: Mapped[int] = mapped_column(Integer, ForeignKey('planets.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    homeworld: Mapped["Planet"] = relationship("Planet", back_populates="species")
    characters: Mapped[list["Character"]] = relationship("Character", back_populates="species")

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "skin_colors": self.skin_colors,
            "hair_colors": self.hair_colors,
            "eye_colors": self.eye_colors,
            "average_lifespan": self.average_lifespan,
            "language": self.language,
            "homeworld_id": self.homeworld_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Character(db.Model):
    __tablename__ = 'characters'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=True)
    mass: Mapped[str] = mapped_column(String(20), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    homeworld_id: Mapped[int] = mapped_column(Integer, ForeignKey('planets.id'), nullable=True)
    species_id: Mapped[int] = mapped_column(Integer, ForeignKey('species.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    homeworld: Mapped["Planet"] = relationship("Planet", back_populates="characters")
    species: Mapped["Species"] = relationship("Species", back_populates="characters")
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="character", cascade="all, delete-orphan")
    film_characters: Mapped[list["FilmCharacter"]] = relationship("FilmCharacter", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld_id": self.homeworld_id,
            "species_id": self.species_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Film(db.Model):
    __tablename__ = 'films'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    episode_id: Mapped[int] = mapped_column(Integer, nullable=True)
    opening_crawl: Mapped[str] = mapped_column(Text, nullable=True)
    director: Mapped[str] = mapped_column(String(100), nullable=True)
    producer: Mapped[str] = mapped_column(String(255), nullable=True)
    release_date: Mapped[Date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    film_characters: Mapped[list["FilmCharacter"]] = relationship("FilmCharacter", back_populates="film", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "title": self.title,
            "episode_id": self.episode_id,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.release_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, ForeignKey('characters.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="favorite_characters")
    character: Mapped["Character"] = relationship("Character", back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "created_at": self.created_at
        }


class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(Integer, ForeignKey('planets.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "created_at": self.created_at
        }


class FilmCharacter(db.Model):
    __tablename__ = 'film_characters'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey('films.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, ForeignKey('characters.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    film: Mapped["Film"] = relationship("Film", back_populates="film_characters")
    character: Mapped["Character"] = relationship("Character", back_populates="film_characters")

    def serialize(self):
        return {
            "id": self.id,
            "film_id": self.film_id,
            "character_id": self.character_id,
            "created_at": self.created_at
        }