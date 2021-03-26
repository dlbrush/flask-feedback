from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect the app to the database"""

    db.app = app
    db.init_app(app)

class Feedback(db.Model):
    """Stores data about feedback left in the app."""

    __tablename__ = 'feedback'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    title = db.Column(
        db.String(100),
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    username = db.Column(
        db.String,
        db.ForeignKey('users.username')
    )

    user = db.relationship('User', backref=db.backref('feedback', cascade="all,delete"))

    @classmethod
    def add(cls, title, content, username):
        """
        Create a new feedback post and commit to the database from the passed data.
        """
        new_post = cls(title=title, content=content, username=username)
        db.session.add(new_post)
        db.session.commit()

    def edit(self, title, content):
        """
        Update the title and content stored to a Feedback instance based on the data passed.
        """
        self.title = title
        self.content = content
        db.session.commit()

class User(db.Model):
    """Defines a user of the app in our database"""

    __tablename__ = 'users'

    username = db.Column(
        db.String(20),
        primary_key = True,
        unique = True
    )

    password = db.Column(
        db.Text,
        nullable = False
    )

    email = db.Column(
        db.String(50),
        nullable = False,
        unique = True
    )

    first_name = db.Column(
        db.String(30),
        nullable = False
    )

    last_name = db.Column(
        db.String(30),
        nullable = False
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """
        Create a hash of the user's password and store that to a User instance to be stored in the database.
        """
        hashed = bcrypt.generate_password_hash(password)
        hashed_text = hashed.decode('utf8')
        return cls(username=username, password=hashed_text, email=email, first_name=first_name, last_name=last_name)

    def authenticate(self, password):
        """
        Check the password passed as an argument against the password saved to this user.
        Returns true if the password is authenticated.
        """
        return bcrypt.check_password_hash(self.password, password)


