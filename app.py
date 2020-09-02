import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm, LoginForm, AddPlantForm, EditPlantForm, TutorialForm, GardenForm
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


#Routes for user methodology
@app.route('/', methods=['GET','POST'])
def landing_page():
    """Basic landing page"""
    form = TutorialForm()

    if form.validate_on_submit():
        which_user = User.query.get_or_404(g.user.id)

        which_user.first_name = form.first_name.data
        which_user.last_name = form.last_name.data
        which_user.profile_pic_url = form.profile_pic_url.data
        which_user.location = form.location.data
        which_user.fully_set_up = True
        

        db.session.add(which_user)
        db.session.commit()
        return redirect('/')

    return render_template('index.html', form=form)

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

        do_login(new_user)

        return redirect('/')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """Log into page and find user"""
    form = LoginForm()

    if form.validate_on_submit():
        which_user = User.authentication(form.username.data, form.password.data)

        if which_user:
            do_login(which_user)
            flash(f'Login succesful!', 'sucess')
            return redirect('/')
        else:
            flash(f'Invalid credentials','danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Log user out and clear g/session"""
    do_logout()
    flash(f'Logout succesful! See ya later')
    return redirect('/')

