### API used for plants: https://trefle.io/ <-- API has become deprecated :(
### API used for weather: https://www.weatherbit.io/api
### API used for images: https://www.flickr.com/services/api/

# Plant Keeper: https://plant-keeper.herokuapp.com/

A web application that allows users to keep track of all of their plants that they own and helps keep them healthy.
Some of the features are:
- Weather/forecast feature 
- Garden feature(user can add plants to a garden)
- Plants feature(user can add and delete plants from garden)
- Reminder feature(remind users if their plants need water, trimming, or repotting)
These features were picked as a starting point for the application.  Most of them help/compliment each other to bring a full experience to the user.

The standard flow goes like this:
- User registers/logins
- User is taken to a page where we collect some more data if they register
- User is then taken to a main page.  If its their first time, we tell them to add plants
-  If not their first time, we show them their dashboard
-  From there a user can either add a new garden, edit a current garden, add plants, remove plants, or search for plants

The following tech is used:
- Flask
- Postgres
- SQLAlchemy
- Python
- Javascript
- Bootstrap
- HTML/CSS

* V2 coming later this year! Check out a sneak preview [here!](https://imgur.com/a/fbQsTiQ)
