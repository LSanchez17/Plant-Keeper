from api_logic import weather_for_watering
from models import User, Plants, Garden
from datetime import date, datetime, timedelta
import pdb

WEATHER_API_KEY_REMOVE_ME = '7c-JHovj1mUW2xTvrfm30aMUZ1W0T9GM0p0wncztwRA'

def get_reminders(user):
    """Compare plant data tied to a user and return it"""
    todays_date = date.today()

    user_plants = Plants.query.filter(Plants.user_id == user.id)

    if not user_plants:
        return
    
    plants_need_water = watering_needs(user_plants, todays_date, user.location)
    plants_need_repotted = repotting_needs(user_plants, todays_date)
    plants_need_trimmed = trimming_needs(user_plants, todays_date)

    reminders = []
    reminders.append(plants_need_water) 
    reminders.append(plants_need_repotted)
    reminders.append(plants_need_trimmed)
        
    return reminders

def watering_needs(plants, date, user_zip):
    """Compares dates for watering needs"""
    need_water = []

    for items in plants:
        if( abs(((trim_dates(items.last_watered) - trim_dates(date)))) > timedelta(days=4) and items.indoor == True):
            need_water.append(items)
        elif( abs(((trim_dates(items.last_watered) - trim_dates(date)))) > timedelta(days=1) and items.indoor == False):
            need_water.append(weather_comparison(items, weather_for_watering(WEATHER_API_KEY_REMOVE_ME, user_zip)))
        else:
            return
    
    return need_water

def repotting_needs(plants, date):
    """Does this plant need to be repotted"""
    need_repotting = []

    for items in plants:
        if( abs((trim_dates(items.last_repotted) - trim_dates(date))) > timedelta(days=270)):
            need_repotting.append(items)

    return need_repotting

def trimming_needs(plants, date):
    """Does this plant need to be trimmed"""
    need_trimmed = []

    for items in plants: 
        if( abs((trim_dates(items.last_trimmed) - trim_dates(date))) > timedelta(days=210)):
            need_trimmed.append(items)

    return need_trimmed


def weather_comparison(plant, date, weather):
    """Compares data for simple watering needs for a list of plants, all plants here are outdoor"""
    weather_rain_codes = [200, 201, 202, 230, 231, 232, 300, 301, 302, 500, 501, 502, 521, 522]

    pdb.set_trace()
    if( abs(((trim_dates(plant.last_watered) - trim_dates(date)))) > timedelta(1) and (weather.data.code not in weather_rain_codes)):
        return plant    

def trim_dates(date):
    """Trims dates from lists to facilitate date comparisons"""
    date = str(date)

    if(len(date) > 10):
        date = date[:10]
        converted = datetime.strptime(date, '%Y-%m-%d')
        return converted
    else:
        converted = datetime.strptime(date, '%Y-%m-%d')
        return converted
