from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="user", cascade="all, delete-orphan")
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None
        }

class Character(db.Model):
    __tablename__ = 'characters'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=True)
    mass: Mapped[str] = mapped_column(String(20), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[str] = mapped_column(String(20), nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(Integer, ForeignKey('characters.id'), nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="favorite_characters")
    character: Mapped["Character"] = relationship("Character", back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(Integer, ForeignKey('planets.id'), nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
