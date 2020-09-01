import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm, AddPlantForm, EditPlantForm, TutorialForm, GardenForm
from models import db, connect_db, User, Plants, Weather, Garden

LOGGED_IN_USER = ""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///plant-keeper'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "123456789")

connect_db(app)

# Handling user instantiation into G object
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to g"""

    if LOGGED_IN_USER in session:
        g.user = User.query.get(session[LOGGED_IN_USER])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[LOGGED_IN_USER] = user.id
    add_user_to_g()


def do_logout():
    """Logout user & remove them from the g"""

    if LOGGED_IN_USER in session:
        del session[LOGGED_IN_USER]
        g.user = None

######################################################


#Routes with no forms
@app.route('/')
def landing_page():
    """Basic landing page"""

    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    """Register a new user"""
    form = RegisterForm()
	
    if form.validate_on_submit():
        try:
            new_user = User.register(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                profile_pic_url=form.pic_url.data
            )

            db.session.commit()

            session['user_id'] = new_user.username

        except IntegrityError:
            flash('Username already exists', 'danger')
            
            return render_template('register.html', form=form)

        do_login(user)

        return redirect('/')

    else:
        return render_template('register.html', form=form)

@app.route('/login')
def login():
    """Log into page and find user"""

    return render_template('login.html')

#######################################################


#Form Routes
