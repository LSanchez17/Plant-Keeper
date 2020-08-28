import os

from flask import Flask, render_template, request, flash, redirect, session, g
# from forms import RegisterForm, AddPlantForm, EditPlantForm
from models import db, connect_db, User, Plants, Weather, Garden

LOGGED_IN_USER = ""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///plant-keeper'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "123456789")

connect_db(app)

# Handling user instantiation into G object
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to g"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    add_user_to_g()


def do_logout():
    """Logout user & remove them from the g"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        g.user = None

######################################################


#Routes with no forms
@route('/')
def landing_page():

    return render_template('index.html')



#######################################################


#Form Routes
