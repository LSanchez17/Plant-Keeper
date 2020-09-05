import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm, LoginForm, AddPlantForm, EditPlantForm, TutorialForm, GardenForm, EditUserInformation
from models import db, connect_db, User, Plants, Weather, Garden
from api_logic import get_weather, search_plants

LOGGED_IN_USER = ""
WEATHER_API_KEY_REMOVE_ME = '8b2d74694d9e4fa0a8f1e9f7bc8f3a35'
PLANT_API_KEY_REMOVE_ME = '7c-JHovj1mUW2xTvrfm30aMUZ1W0T9GM0p0wncztwRA'


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
    """Basic landing page, shows login/register on template if not stored in local G object
       If stored in local g object, we show them a tutorial form so we can set up user account better
       Once user is set up, they can begin doing plant stuff
    """
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
            flash(f'Login succesful!', 'success')
            return redirect('/')
        else:
            flash(f'Invalid credentials','danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Log user out and clear g/session"""
    do_logout()
    flash(f'Logout succesful! See ya later','success')
    return redirect('/')

#####################################################
#Routes for plants
@app.route('/<int:user_id>/plants')
def plant_page(user_id):
    """Displays plants tied to this user"""
    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect("/")

    which_user = User.query.get_or_404(user_id)
    which_plants = Plants.query.filter(Plants.user_id == which_user.id)

    return render_template('plants/plants_page.html', plants=which_plants)

@app.route('/<int:user_id>/plants/add', methods=['GET','POST'])
def add_plants(user_id):
    """Adds a plant to this user's account"""
    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect("/")
    
    which_user = User.query.get_or_404(user_id)
    form = AddPlantForm()

    if form.validate_on_submit():
        new_plant = Plants(
                    plant_name = form.plant_name.data,
                    plant_birthday = form.plant_birthday.data,
                    last_watered = form.last_watered.data or form.last_watered.default,
                    last_trimmed = form.last_trimmed.data or form.last_trimmed.default,
                    last_repotted = form.last_repotted.data or form.last_repotted.default,
                    indoor = form.indoor.data,
                    user_id = which_user.id
                    )
        
        db.session.add(new_plant)
        db.session.commit()
    
        flash('Plant added successfully!', 'success')
        return redirect(f'/{g.user.id}/plants')
    else:
        return render_template('/plants/add_plant.html', form=form)

    return render_template('/plants/add_plant.html', form=form)

@app.route('/<int:user_id>/plants/edit/<int:plant_id>', methods=['GET','POST'])
def edit_plants(user_id, plant_id):
    """Lets user update information on current plants attached to their account"""
    which_user = User.query.get_or_404(user_id)

    form = EditPlantForm()

    if form.validate_on_submit():
        which_plant = Plants.query.get_or_404(plant_id)

        which_plant.last_watered = form.last_watered.data
        which_plant.last_trimmed = form.last_trimmed.data
        which_plant.last_repotted = form.last_repotted.data
        which_plant.indoor = form.indoor.data or False

        db.session.add(which_plant)
        db.session.commit()

        flash('Plant editted successfully!', 'Sucess')
        return redirect(f'/{g.user.id}/plants')
    
    return render_template('/plants/edit_plants.html', form=form)

###########################################################################
#USER ACCOUNT EDIT INFORMATION
@app.route('/<int:user_id>/account')
def view_account(user_id):
    """View user account"""
    which_user = User.query.get_or_404(user_id)
    list_of_plants = which_user.plants

    return render_template('/user/user_view.html', user=which_user, plant_list=list_of_plants)

@app.route('/<int:user_id>/account/edit')
def edit_account(user_id):
    """Edit user information"""
    which_user = User.query.get_or_404(user_id)
    form = EditUserInformation()

    if form.validate_on_submit():
        which_user.email = form.email.data or which_user.email
        which_user.first_name = form.first_name.data or which_user.first_name
        which_user.last_name = form.last_name.data or which_user.last_name
        which_user.profile_pic_url = form.profile_pic_url.data or which_user.profile_pic_url
        which_user.location = form.location.data or which_user.location

        db.session.add(which_user)
        db.session.commit()

        flash('Information updated!', 'success')
        return redirect(f'/{g,user.id}/account')

    return render_template('/user/user_edit.html', form=form)


###########################################################################
# Weather API reporting
@app.route('/weather')
def general_weather():
    """Shows current forecast"""
    weather = get_weather(WEATHER_API_KEY_REMOVE_ME)
    print(weather)
    return render_template('/weather/general_weather.html', weather=weather.json())

###########################################################################
@app.route('/<int:user_id>/plants/search')
def search_for_plants(user_id):
    """Search for plants and add them to your account"""

    return render_template('/plants/search.html')

@app.route('/api/plants/search', methods=['GET'])
def return_searched_plants(plant):
    """Calls python to make serve request, avoiding COORS NIGHTMARES"""
    plant = request.json
    
    list_of_plants = search_plants(plant, PLANT_API_KEY_REMOVE_ME)

    print(list_of_plants)

    return list_of_plants
###########################################################################
###########################################################################
########################DELETE ME AFTER HEROKU DEPLOYMENT##################

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req