import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = ""
database_path ="postgres://{}:{}@{}/{}".format('postgres', 'postgres','flask-db.csljbjej7s5s.us-west-2.rds.amazonaws.com', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


class VehicleModel(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())
    vehicle_type = db.Column(db.String())

    def __init__(self, brand, model, doors, vehicle_type):
        self.brand = brand
        self.model = model
        self.doors = doors
        self.vehicle_type = vehicle_type

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Vehicle {self.brand}>"