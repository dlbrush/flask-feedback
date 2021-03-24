from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "f33db4ck"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def redirect_root():
    return redirect('/register')

@app.route('/register', methods=['POST', 'GET'])
def registration_form():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            flash("Username already taken! Please try again.")
            return redirect('/register')

        session['username'] = username
        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login_form():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.authenticate(password=password):
                session['username'] = username
                return redirect(f'/users/{username}')
            else:
                form.password.errors = ['Invalid password.']
        else:
            form.username.errors = ['Invalid username.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')

@app.route('/users/<username>')
def show_user(username):
    if 'username' in session:
        user = User.query.get_or_404(username)
        feedback = user.feedback
        return render_template('user.html', user=user, feedback=feedback)
    else:
        flash("Please log in first.")
        return redirect('/login')