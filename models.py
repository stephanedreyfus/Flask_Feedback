from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    ''' Creates user, takes in password, hashes for storage
    and authentication. '''

    username = db.Column(db.String(20),
                         primary_key=True,
                         unique=True,)
    password = db.Column(db.Test, nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)gst
