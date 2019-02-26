from flask import Flask, render_template, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)
# db.create_all()

debug = DebugToolbarExtension(app)


@app.route('/')
def redirect_to_register():
    """ Redirects client to register """

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def show_or_submit_register_form():
    """ Register user OR show registration form """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # BONUS: we can check to see if this login already exists
        # form.username.errors = ['Username already exists!]

        user = User.register(username=username,
                             password=password,
                             email=email,
                             first_name=first_name,
                             last_name=last_name,
                             )

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['Incorrect username/password']

    else:
        return render_template("login.html", form=form)
