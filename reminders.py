from api_logic import get_weather
from models import User, Plants, Garden
from datetime import date

WEATHER_API_KEY_REMOVE_ME = '7c-JHovj1mUW2xTvrfm30aMUZ1W0T9GM0p0wncztwRA'

def get_reminders(user):
    """Compare plant data tied to a user and return it"""
    todays_date = date.today()

    user_plants = Plants.query.filter(Plants.user_id == user.id)

    plants_need_water = watering_needs(user_plants, todays_date, user.location)
    plants_need_repotted = repotting_needs(user_plants, todays_date)
    plants_need_trimmed = trimming_needs(user_plants, todays_date)

    reminders = []
    reminders.append(plants_need_water, plants_need_repotted, plants_need_trimmed)
        
    return reminders

def watering_needs(plants, date, user_zip):
    """Compares dates for watering needs"""
    need_water = []

    for items in plants:
        if((items.last_watered - date > 4) and items.indoor == True):
            need_water.append(items)
        elif((items.last_watered - date > 1) and items.indoor == False):
            need_water.append(weather_comparison(plants, get_weather(WEATHER_API_KEY_REMOVE_ME, date, user_zip)))
        else:
            need_water.append('No plants need water!')
    
    return need_water

def repotting_needs(plants, date):
    """Does this plant need to be repotted"""
    need_repotting = []

    for items in plants:
        if((items.last_repotted - date > 270)):
            need_repotting.append(items)
        else:
            need_repotting.append('No repotting needed')

    return need_repotting

def trimming_needs(plants, date):
    """Does this plant need to be trimmed"""
    need_trimmed = []

    for items in plants:
        if((items.last_trimmed - date > 210)):
            need_trimmed.append(items)

    return need_trimmed


def weather_comparison(plants, date, weather):
    """Compares data for simple watering needs for a list of plants, all plants here are outdoor"""
    print(weather)
    need_water = []

    for items in plants:
        if((plants.last_watered - date > 1)):
            print(item)
        else:
            need_water.append('No watering needed today!')
    
    return need_water


def trimm_dates(date):
    """Trims dates from lists to facilitate date comparisons"""