import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = ""
#database_path ="postgres://{}:{}@{}/{}".format('postgres', 'postgres','flask-db.csljbjej7s5s.us-west-2.rds.amazonaws.com', database_name)
database_path = 'mysql+pymysql://flask:Mypass1234_$*@localhost/flask_tutorial'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))
    model = db.Column(db.String(255))
    year = db.Column(db.Integer())
    doors = db.Column(db.Integer())
    power = db.Column(db.Integer())
    licence = db.Column(db.String(255))
    transmission = db.Column(db.Integer())
    vtype = db.Column(db.String(255))
    category = db.Column(db.String(255))    

    def __init__(self, brand, model, doors, vtype, year, power, licence, transmission, category):
        self.brand = brand
        self.model = model
        self.doors = doors
        self.vtype = vtype
        self.year = year
        self.power = power
        self.licence = licence
        self.transmission = transmission
        self.category = category

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


class Utilization(db.Model):
    __tablename__ = 'utilizations'

    id = db.Column(db.Integer, primary_key=True)
    ref_vehicle = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())

    user = db.relationship('User', backref="user", lazy=True)
    

    def __init__(self, ref_vehicle, start_time, end_time):
        self.ref_vehicle = ref_vehicle
        self.start_time = start_time
        self.end_time = end_time

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


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    name = db.Column(db.String(255))
    enrolment_time = db.Column(db.DateTime())
    level = db.Column(db.String(255))
    licences = db.Column(db.String(255))


    def __init__(self, username, name, enrolment_time, level):
        self.username = username
        self.name = name
        self.enrolment_time = enrolment_time
        self.level = level
        self.licences = licences

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.name}>"
