from flask import Flask, render_template, session, redirect, flash
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

        return redirect('/users/<username>')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """ Handle displaying and submitting login form """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect('/users/<username>')
        else:
            form.username.errors = ['Incorrect username/password']

    return render_template("login.html", form=form)


@app.route('/users/<username>')
def show_user_details_page(username):
    """ Handle displaying secret page only for logged in users,
    redirect everyone else. """
    cur_user = session.get('username')
    user = User.query.filter_by(username=cur_user).first()

    if user:

        return render_template('user_details.html', user=user)

    else:
        flash('You must be logged in to see user details!')
        return redirect('/')


@app.route('/logout')
def log_out():
    """ Handle user logging out, clearing session and redirecting back to '/login'"""

    session.pop("username")

    return redirect("/login")