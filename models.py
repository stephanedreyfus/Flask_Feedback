from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    ''' Creates user, takes in password, hashes for storage
    and authentication. '''

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         unique=True,)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register the user with hashed
            password & return the user instance."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # returning the instance of user with username and hased pwd
        return cls(username=username,
                   password=hashed_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name,
                   )
