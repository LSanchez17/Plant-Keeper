from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional

from datetime import date

class RegisterForm(FlaskForm):
    """Form for registering messages."""

    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    pic_url = StringField('Profile Picture URL:', validators=[Optional()])

class LoginForm(FlaskForm):
    """Form for logging in messages."""

    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])

class EditUserInformation(FlaskForm):
    """Form for editing user information"""

    email = StringField('Email: ', validators=[Optional(), Email()])
    first_name = StringField('First name: ', validators=[Optional()])
    last_name = StringField('Last name: ', validators=[Optional()])
    profile_pic_url = StringField('New profile pic URL: ', validators=[Optional()])
    location = IntegerField('Zip Code: ', validators=[Optional()])

class AddPlantForm(FlaskForm):
    """Form for adding a plant to user's garden"""

    plant_name = StringField('Plant Name(common or scientific):', validators=[DataRequired()])
    plant_birthday = StringField('Date of purchase(Y:M:D):', default=date.today(), validators=[DataRequired()])
    last_watered = DateField('Last date watered(Y:M:D)', default=date.today(), validators=[Optional()])
    last_trimmed = DateField('Last date trimmed(Y:M:D)', default=date.today(), validators=[Optional()])
    last_repotted = DateField('Last date repotted(Y:M:D)', default=date.today(), validators=[Optional()])
    indoor = BooleanField('Indoor plant?', validators=[Optional()])

class EditPlantForm(FlaskForm):
    """Login form."""

    last_watered = DateField('Date last watered', validators=[Optional()])
    last_trimmed = DateField('Date last trimmed', validators=[Optional()])
    last_repotted = DateField('Date last repotted', validators=[Optional()])
    indoor = BooleanField('Indoor plant?', validators=[Optional()])
    # garden_residency = SelectField('Which garden?', validators=[DataRequired()])

class TutorialForm(FlaskForm):
    """Tutorial form for inserting basic user information"""
    first_name = StringField('First name:', validators=[DataRequired()])
    last_name = StringField('Last name:', validators=[DataRequired()])
    profile_pic_url = StringField('Profile picture URL', validators=[Optional()])
    location = IntegerField('Zip Code', validators=[DataRequired()])

class GardenForm(FlaskForm):
    """For for editing garden"""
    garden_name = StringField('Garden name:', validators=[DataRequired()])
    description = StringField('Garden description:', validators=[DataRequired()])

class EditGardenForm(FlaskForm):
    """Edit garden name and description"""
    garden_name = StringField('Garden name:', validators=[Optional()])
    description = StringField('Garden description:', validators=[Optional()])

class NewPlantForGarden(FlaskForm):
    """Form for adding a platn to a specific garden."""

    plant = SelectField('Pick a plant to add', coerce=int, validators=[DataRequired()])
