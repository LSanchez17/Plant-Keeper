"""Models for capstone"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

DEFAULT_IMG = '/static/user_default.png'

class User(db.Model):
    """User model"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    profile_pic_url = db.Column(db.Text, default='/static/user_default.png')
    location = db.Column(db.Integer)
    password = db.Column(db.Text, nullable=False)
    fully_set_up = db.Column(db.Boolean, default=False)

    plants = db.relationship('Plants', backref='owner')
    weather = db.relationship('Weather', backref='owner')

    def __repr__(self):
        """Tell on yourself"""
        return f'[User: #{self.id}, {self.username}, {self.email}, {self.fully_set_up}]'

    @classmethod
    def register(cls, username, email, password, profile_pic_url):
        """Register a new user"""

        password_hash = bcrypt.generate_password_hash(password).decode('utf8')

        user = User(username=username, email=email, profile_pic_url=profile_pic_url or DEFAULT_IMG, password=password_hash)

        db.session.add(user)
        return user

    @classmethod
    def authentication(cls, username, password):
        """Do you have a license for that account sir/maam/entity"""

        user = cls.query.filter_by(username=username).first()

        if user:
            authorized = bcrypt.check_password_hash(user.password, password)
            if authorized:
                return user
        return False

class Plants(db.Model):
    """Plant model"""

    __tablename__ = 'plant'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plant_name = db.Column(db.Text, nullable=False)
    plant_birthday = db.Column(db.DateTime)
    last_watered = db.Column(db.DateTime, default=datetime.utcnow())
    last_trimmed = db.Column(db.DateTime, default=datetime.utcnow())
    last_repotted = db.Column(db.DateTime, default=datetime.utcnow())
    indoor = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    gardens = db.relationship('DescribeGarden', secondary='garden')


    def __repr__(self):
        """Quick plant info"""
        return f'[Plant: #{self.id}, {self.plant_name}, {self.user_id}]'

class Weather(db.Model):
    """Weather data model"""

    __tablename__ = 'weather'

    location = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    forecast = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __repr__(self):
        """Quick weather check"""
        return f'[Weather: {self.location}: {self.date}-{self.forecast}]'

class DescribeGarden(db.Model):
    """A garden to be combined with plants for better data visualization"""

    __tablename__ = 'garden_holder'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)

    plants = db.relationship('Plants', secondary='garden')

class Garden(db.Model):
    """
    Many plants can be long to many gardens, and user can have many 
    gardens and many plants all at once
    """

    __tablename__ = 'garden'

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id', ondelete='CASCADE'))
    garden_id = db.Column(db.Integer, db.ForeignKey('garden_holder.id', ondelete='CASCADE'))

    garden_desc = relationship(DescribeGarden, backref=backref('garden', cascade='all, delete-orphan'))
    plant = relationship(Plants, backref=backref('garden', cascade='all, delete-orphan'))

    def __repr__(self):
        """Garden info"""
        return f'[Garden: {self.name}-{self.user}, {self.plant_id}]'

def connect_db(app):
    """Connect this database"""

    db.app = app
    db.init_app(app)