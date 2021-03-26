from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email
from wtforms.fields.html5 import EmailField

class RegistrationForm(FlaskForm):
    """Form that allows the user to register for an account"""

    username = StringField("Username", validators=[Length(max=30, message="Username can't be longer than 30 characters."), InputRequired(message="Please enter a unique username.")])

    password = PasswordField("Password", validators=[InputRequired()])

    email = EmailField("Email", validators=[Email(message="Please enter a valid email.")])

    first_name = StringField("First Name", validators=[Length(max=30, message="Name can't be longer than 30 characters."), InputRequired(message="Please enter your first name")])

    last_name = StringField("Last Name", validators=[Length(max=30, message="Name can't be longer than 30 characters."), InputRequired(message="Please enter your last name")])

class LoginForm(FlaskForm):
    """Form that just takes a username and password to log the user in."""
    username = StringField("Username", validators=[InputRequired(message="Enter your username.")])

    password = PasswordField("Password", validators=[InputRequired(message="Enter a password.")])

class FeedbackForm(FlaskForm):
    """Form that takes the title and content of a feedback post for a user."""
    title = StringField("Title", validators=[InputRequired(message="Please enter a title."), Length(max=100, message="Title must be less than 100 characters")])

    content = TextAreaField("Feedback", validators=[InputRequired(message="Please add your feedback.")])
        