from flask import Flask, request, render_template, session, bcrypt
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)
# db.create_all()

debug = DebugToolbarExtension(app)


