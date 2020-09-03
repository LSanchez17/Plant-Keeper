from forms import RegisterForm, LoginForm, AddPlantForm, EditPlantForm, TutorialForm, GardenForm
from models import db, connect_db, User, Plants, Weather, Garden

def get_weather():
    """
    Makes a request to API weather, stores it to server database, and returns the query result
    """
    weather = True

    return weather

def search_plants():
    """Returns request to search plants and lists them all"""
    list_plants = []

    return list_plants