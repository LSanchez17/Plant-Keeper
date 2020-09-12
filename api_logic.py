import requests

def get_weather(APIKey, zip, short):
    """
    Makes a request to API weather, stores it to server database, and returns the query result
    """
    if(short):
        weather = requests.get('https://api.weatherbit.io/v2.0/current', params={'postal_code': zip, 'units': 'I', 'Key': APIKey})
    else:
        weather = requests.get('http://api.weatherbit.io/v2.0/forecast/daily', params={'postal_code': zip, 'days': 3, 'units': 'I', 'Key': APIKey})
    return weather

def weather_for_watering(APIKey, zip):
    """Returns a small 3 day forecast for determining if we need to water a plant"""
    weather = request.get('htt[://api.weather.io/v2.0/forecast/daily', params={'postal_code': zip, 'days': 3, 'units': 'I', 'Key':APIKey})

    return weather

def search_plants(plant, APIKey):
    """Returns request to search plants and lists them all"""
    response = requests.get('https://trefle.io/api/v1/plants/search', 
                            params={'q': plant}, 
                            headers={'Authorization': APIKey})

    return response


def search_images(query, APIKey):
    """Search through a custom search bar through google, get images back"""
    response = requests.get('https://api.flickr.com/services/rest',
                            params={'method': 'flickr.photos.search',
                                    'api_key': APIKey,
                                    'text': query,
                                    'per_page': 1,
                                    'format': 'json',
                                    'nojsoncallback': 1        
                            })

    return response