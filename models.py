from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect the app to the database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Defines a user of the app in our database"""

    __tablename__: "users"

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
        hashed = bcrypt.generate_password_hash(password)
        hashed_text = hashed.decode('utf8')
        return cls(username=username, password=hashed_text, email=email, first_name=first_name, last_name=last_name)

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password, password)
