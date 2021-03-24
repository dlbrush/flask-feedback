from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from wtforms.fields.html5 import EmailField

class RegistrationForm(FlaskForm):
    """Form that allows the user to register for an account"""

    username = StringField(validators=[Length(max=30, message="Username can't be longer than 30 characters."), InputRequired(message="Please enter a unique username.")])

    password = PasswordField(validators=[InputRequired()])

    email = EmailField(validators=[Email(message="Please enter a valid email.")])

    first_name = StringField(validators=[Length(max=30, message="Name can't be longer than 30 characters."), InputRequired(message="Please enter your first name")])

    last_name = StringField(validators=[Length(max=30, message="Name can't be longer than 30 characters."), InputRequired(message="Please enter your last name")])

class LoginForm(FlaskForm):
    """Form that just takes a username and password to log the user in."""
    username = StringField(validators=[InputRequired("Enter a username.")])

    password = PasswordField(validators=[InputRequired("Enter a password.")])