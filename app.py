import os
import pdb

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from forms import RegisterForm, LoginForm, AddPlantForm, EditPlantForm, TutorialForm, GardenForm, EditUserInformation, NewPlantForGarden
from models import db, connect_db, User, Plants, Weather, Garden, DescribeGarden
from api_logic import get_weather, search_plants, search_images
from reminders import get_reminders

LOGGED_IN_USER = "logged_in_user"
WEATHER_API_KEY_REMOVE_ME = os.environ.get('WEATHER_API')
PLANT_API_KEY_REMOVE_ME = os.environ.get('PLANT_API')
API_FLICKR_REMOVE_ME = os.environ.get('FLICKR_API')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///plant-keeper'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "123456789")

connect_db(app)
######################################################
# Handling user instantiation into G object
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to g"""

    if LOGGED_IN_USER in session:
        g.user = User.query.get_or_404(session[LOGGED_IN_USER])
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
@app.route('/')
def landing():
    """Landing Page"""

    if g.user and g.user.fully_set_up:
        return redirect(f'/hub/{g.user.id}')
    elif g.user and g.user.fully_set_up == False:
        return redirect('/tutorial')
    else:
        return render_template('landing.html')

@app.route('/tutorial', methods=['GET','POST'])
def tutorial():
    """Tutorial for setting up user correctly"""

    if g.user and (session[LOGGED_IN_USER] != 'logged in user'):
        if g.user.fully_set_up:
            return redirect(f'/hub/{g.user.id}')
        else:
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
                return redirect(f'/hub/{g.user.id}')
            else:
                return render_template('tutorial.html', form=form)
    return redirect('/')

@app.route('/hub/<int:user_id>')
def hub_page(user_id):
    """Main user hub. Contains user information like their gardens, quick weather, and reminders"""

    if g.user or (session[LOGGED_IN_USER] == 'logged in user'):

        try:
            which_user = User.query.get_or_404(user_id)
            weather = get_weather(WEATHER_API_KEY_REMOVE_ME, g.user.location, False)
            reminders = get_reminders(which_user)
            garden = which_user.garden

            data_list = [weather.json(), reminders, garden]

            return render_template('hub.html', data=data_list)
        except:
            message = 'Please add a plant to your account to start'
            return render_template('hub.html', error=message)
    return redirect('/')

@app.route('/register', methods=['GET','POST'])
def register():
    """Register a new user"""
    if g.user:
        return redirect(f'/hub/{g.user.id}')

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

        except IntegrityError:
            flash('Username already exists', 'danger')
            return render_template('register.html', form=form)
        
        
        session['user_id'] = new_user.username
        do_login(new_user)

        return redirect('/tutorial')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """Log into page and find user"""
    if g.user:
        return redirect(f'/hub/{g.user.id}')

    form = LoginForm()

    if form.validate_on_submit():
        which_user = User.authentication(form.username.data, form.password.data)

        if which_user:
            do_login(which_user)
            flash(f'Login succesful!', 'success')

            return redirect('/tutorial')
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
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    which_user = User.query.get_or_404(user_id)
    which_plants = Plants.query.filter(Plants.user_id == which_user.id)

    return render_template('plants/plants_page.html', plants=which_plants)

@app.route('/<int:user_id>/plants/add', methods=['GET','POST'])
def add_plants(user_id):
    """Adds a plant to this user's account"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')
    
    which_user = User.query.get_or_404(user_id)
    form = AddPlantForm()

    if form.validate_on_submit():
        new_plant = Plants(
                    plant_name = form.plant_name.data,
                    plant_birthday = form.plant_birthday.data,
                    last_watered = form.last_watered.data or form.last_watered.default,
                    last_trimmed = form.last_trimmed.data or form.last_trimmed.default,
                    last_repotted = form.last_repotted.data or form.last_repotted.default,
                    indoor = form.indoor.data or False,
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
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    which_user = User.query.get_or_404(user_id)

    form = EditPlantForm()

    if form.validate_on_submit():
        which_plant = Plants.query.get_or_404(plant_id)

        which_plant.last_watered = form.last_watered.data or which_plant.last_watered
        which_plant.last_trimmed = form.last_trimmed.data or which_plant.last_trimmed
        which_plant.last_repotted = form.last_repotted.data or which_plant.last_repotted
        which_plant.indoor = form.indoor.data or False

        db.session.add(which_plant)
        db.session.commit()

        flash('Plant editted successfully!', 'Success')
        return redirect(f'/{g.user.id}/plants')
    
    return render_template('/plants/edit_plants.html', form=form)

###########################################################################
#Routes for user information
@app.route('/<int:user_id>/account')
def view_account(user_id):
    """View user account"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    which_user = User.query.get_or_404(user_id)
    list_of_plants = which_user.plants
    garden_number = which_user.garden

    return render_template('/user/user_view.html', user=which_user, plant_list=list_of_plants, gardens=garden_number)

@app.route('/<int:user_id>/account/edit', methods=['GET','POST'])
def edit_account(user_id):
    """Edit user information"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

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
        return redirect(f'/{g.user.id}/account')

    return render_template('/user/user_edit.html', form=form)

@app.route('/<int:user_id>/account/delete', methods=['POST'])
def delete_account(user_id):
    """Delete user account"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    which_garden = User.query.get_or_404(user_id)
    
    db.session.delete(which_garden)
    db.session.commit()
    
    do_logout()
    flash('Account Deleted', 'success')
    
    return redirect('/')

###########################################################################
# Weather API reporting
@app.route('/weather')
def general_weather():
    """Shows current forecast"""
    weather = get_weather(WEATHER_API_KEY_REMOVE_ME, g.user.location, True)

    return render_template('/weather/general_weather.html', weather=weather.json())

###########################################################################
#Routes for plant search
@app.route('/<int:user_id>/plants/search')
def search_for_plants(user_id):
    """Search for plants and add them to your account"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    return render_template('/plants/search.html')

###########################################################################
#Routes for a API endpoint for getting results from a search endpoint
#Allows for adding plants to account, getting images,
@app.route('/api/plants/search', methods=['GET'])
def return_searched_plants():
    """Calls python to make serve request, avoiding COORS NIGHTMARES"""
    plant = request.args.get('q')
    
    list_of_plants = search_plants(plant, PLANT_API_KEY_REMOVE_ME)

    return list_of_plants.json()


@app.route('/api/plants/images', methods=['GET'])
def return_image_from_bing():
    """Get images from flickr"""
    query = request.args.get('q')

    image_chosen = search_images(query, API_FLICKR_REMOVE_ME)

    return image_chosen.json()

@app.route('/api/plants/add', methods=['POST'])
def add_plant_to_user():
    """Add plant to user account"""
    query = request.json

    new_plant = Plants(plant_name = query['hiddenData'], user_id = g.user.id)
        
    db.session.add(new_plant)
    
    try:
        db.session.commit()
        succesful = {'message': 'Added to account!'}
        return jsonify(succesful)
    except:
        unsuccesful = {'message': 'Error while adding'}
        return jsonify(unsuccesful) 
    
@app.route('/api/plants/delete/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    """Delete plant from user"""
    which_plant = Plants.query.get_or_404(plant_id)
    message = {'message': 'Plant Removed!'}

    db.session.delete(which_plant)
    db.session.commit()

    return jsonify(message)

###########################################################################
#Garden Routes
@app.route('/garden/add', methods=['GET', 'POST'])
def add_garden():
    """Add a garden to user account, a collection of plants"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    form = GardenForm()
    
    if form.validate_on_submit():
        new_garden = DescribeGarden(name=form.garden_name.data, description=form.description.data, user_id=g.user.id)

        db.session.add(new_garden)
        db.session.commit()
        
        flash('Added a new garden!', 'success')
        return redirect(f'/hub/{g.user.id}')

    return render_template('/garden/add_garden.html', form=form)

@app.route('/garden/<int:garden_id>', methods=['GET','POST'])
def show_garden(garden_id):
    """Show current garden"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    which_garden = DescribeGarden.query.get_or_404(garden_id)
    which_user = User.query.get_or_404(g.user.id)
    which_plants = which_user.plants
    form = NewPlantForGarden()

    already_in_garden = [plant.id for plant in which_garden.plants]
    form.plant.choices = (db.session.query(Plants.id, Plants.plant_name).filter(Plants.id.notin_(already_in_garden)).filter(Plants.user_id == which_user.id).all())

    if form.validate_on_submit():
        plant = form.plant.data
        add_to_garden = Garden(plant_id=plant, garden_id=which_garden.id)

        db.session.add(add_to_garden)
        db.session.commit()

        flash(f'Plant added to {which_garden.name} garden!', 'success')
        return redirect(f'/hub/{g.user.id}')

    return render_template('/garden/garden.html', garden=which_garden, plants=which_plants, form=form)

@app.route('/garden/<int:garden_id>/edit', methods=['GET','POST'])
def edit_garden(garden_id):
    """Edit garden name and description"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    form = GardenForm()
    which_garden = DescribeGarden.query.get_or_404(garden_id)

    if form.validate_on_submit():
        which_garden = DescribeGarden.query.get_or_404(garden_id)

        which_garden.name = form.garden_name.data or which_garden.name
        which_garden.description = form.description.data or which_garden.description

        db.session.add(which_garden)
        db.session.commit()

        flash(f'Edited garden: {which_garden.name}', 'success')
        return redirect(f'/hub/{g.user.id}')
    
    return render_template('/garden/edit_garden.html', form=form, garden=which_garden)

@app.route('/garden/<int:garden_id>/delete', methods=['POST'])
def delete_garden(garden_id):
    """Delete garden user has"""
    if not g.user or (session[LOGGED_IN_USER] == 'logged in user'):
        flash('Access unauthorized', 'danger')
        return redirect('/')

    which_garden = DescribeGarden.query.get_or_404(garden_id)

    db.session.delete(which_garden)
    db.session.commit()
   
    flash('Garden deleted', 'success')
    return redirect(f'/hub/{g.user.id}')

@app.errorhandler(404)
def page_not_found(err):
    """Page non existent"""

    return render_template('404.html'), 404

