from forms import RegisterForm, LoginForm, AddPlantForm, EditPlantForm, TutorialForm, GardenForm
from models import db, connect_db, User, Plants, Weather, Garden

import requests

def get_weather(APIKey):
    """
    Makes a request to API weather, stores it to server database, and returns the query result
    """
    weather = requests.get('https://api.weatherbit.io/v2.0/current', params={'city': 'Indianapolis', 'Key': f'{APIKey}' })

    return weather

def search_plants(plant, APIKey):
    """Returns request to search plants and lists them all"""
    response = requests.get('https://trefle.io/api/v1/plants/search', params={'q': plant, 'Key': APIKey})

    return response