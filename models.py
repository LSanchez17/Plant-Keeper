"""Models for capstone"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

class Plants(db.Model):

    __tablename__ = 'plants'



class Weather(db.Model):

    __tablename__ = 'weather'


class Garden(db.Model):

    __tablename__ = 'garden'


