from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
class Favorites(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=True)
    
    user: Mapped["Users"] = relationship(back_populates="favorites")
    favorite_people: Mapped["People"] = relationship(back_populates="favorites")
    favorite_planets: Mapped["Planets"] = relationship(back_populates="favorites")
    favorite_species: Mapped["Species"] = relationship(back_populates="favorites")
    favorite_vehicles: Mapped["Vehicles"] = relationship(back_populates="favorites")
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
    
class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    gender: Mapped[str] = mapped_column(String(120))
    skin_color: Mapped[str] = mapped_column(String(120))
    hair_color: Mapped[str] = mapped_column(String(120))
    height: Mapped[int] = mapped_column(Integer())
    eye_color: Mapped[str] = mapped_column(String(120))
    mass: Mapped[int] = mapped_column(Integer())

    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"))
    species: Mapped["Species"] = relationship("Species", back_populates="members")

    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    homeworld: Mapped["Planets"] = relationship(back_populates="residents")

    pilots = relationship("Pilots", back_populates="person")

    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="favorite_people")

class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    climate:  Mapped[str] = mapped_column(String(120))
    surface_water: Mapped[int] = mapped_column(Integer())
    diameter: Mapped[int] = mapped_column(Integer())
    gravity: Mapped[str] = mapped_column(String(120))
    orbital_period: Mapped[int] = mapped_column(Integer())
    population: Mapped[int] = mapped_column(Integer())
    
    residents: Mapped[list["People"]] = relationship(back_populates="homeworld")
    fauna: Mapped[list["Species"]] = relationship(back_populates="homeworld")
    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="favorite_planets")

class Species(db.Model):
    __tablename__ = "species"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    classification: Mapped[str] = mapped_column(String(120))
    designation: Mapped[str] = mapped_column(String(120))
    eye_colors: Mapped[str] = mapped_column(String(120))
    skin_colors: Mapped[str] = mapped_column(String(120))
    language: Mapped[str] = mapped_column(String(120))
    hair_colors: Mapped[str] = mapped_column(String(120))
    average_lifespan:  Mapped[int] = mapped_column(Integer())
    average_height:  Mapped[int] = mapped_column(Integer())
    
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    homeworld: Mapped["Planets"] = relationship("Planets", back_populates="fauna")

    members: Mapped[list["People"]] = relationship("People", back_populates="species")

    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="favorite_species")

class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    consumables: Mapped[str] = mapped_column(String(120))
    cargo_capacity: Mapped[int] = mapped_column(Integer())
    max_atmosphering_speed: Mapped[int] = mapped_column(Integer())
    crew: Mapped[int] = mapped_column(Integer())
    length: Mapped[int] = mapped_column(Integer())
    model: Mapped[str] = mapped_column(String(120))
    vehicle_class: Mapped[str] = mapped_column(String(120))

    pilots = relationship("Pilots", back_populates="vehicle")

    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="favorite_vehicles")

class Pilots(db.Model): #association table for people and vehicles
    __tablename__ = "pilots"
    person_id = mapped_column(ForeignKey("people.id"), primary_key=True)
    vehicle_id = mapped_column(ForeignKey("vehicles.id"), primary_key=True)

    person = relationship("People", back_populates="pilots")
    vehicle = relationship("Vehicles", back_populates="pilots")

