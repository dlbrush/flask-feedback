from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm
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
    """Redirect the user to the registration page if they go to the root route."""
    return redirect('/register')

@app.route('/register', methods=['POST', 'GET'])
def registration_form():
    """
    Show the registration form.
    On form submission, process the data and create a new user from the data passed.
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User.register(username=form.username.data, password=form.password.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            flash("Username already taken! Please try again.")
            return redirect('/register')

        session['username'] = new_user.username
        flash('Welcome!')
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login_form():
    """
    Show the login form.
    On submission, confirm that the user's password is correct for the username entered and redirect to the user's page.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.authenticate(password=form.password.data):
                flash('Sucessfully logged in!')
                session['username'] = user.username
                return redirect(f'/users/{user.username}')
            else:
                form.password.errors = ['Invalid password.']
        else:
            form.username.errors = ['Invalid username.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Remove the username from the session and redirect to the root route."""
    session.pop('username')
    flash('Sucessfully logged out!')
    return redirect('/')

@app.route('/users/<username>')
def show_user(username):
    """
    If the user is logged in, show info and feedback for the user at the given username.
    """
    if 'username' in session:
        user = User.query.get_or_404(username)
        feedback = user.feedback
        return render_template('user.html', user=user, feedback=feedback)
    else:
        flash("Please log in first.")
        return redirect('/login')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """
    If the user is logged in with the user name in the URL, delete the user and redirect to the root route.
    """
    user = User.query.get_or_404(username)
    if 'username' in session and session['username'] == username:
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted.')
        session.pop('username')
        return redirect('/')
    else:
        flash('You do not have permission to delete this user.')
        return redirect(f'/users/{username}')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """
    If the user is logged in with the user name in the URL, show a form to add feedback for that user.
    On form submission, create a new piece of feedback and redirect to the user's page.
    """
    user = User.query.get_or_404(username)
    if 'username' in session and session['username'] == username:
        form = FeedbackForm()
        if form.validate_on_submit():
            Feedback.add(title=form.title.data, content=form.content.data, username=username)
            flash('Feedback added!')
            return redirect(f'/users/{username}')
        else:
            return render_template('add-feedback.html', form=form, username=username)
    else:
        flash("You are not authorized to add feedback for this user.")
        return redirect(f'/users/{username}')

@app.route('/feedback/<int:post_id>/update', methods=['GET', 'POST'])
def update_feedback(post_id):
    """
    If the user is logged in with the username associated with the post in the route, show a form to update that feedback post.
    The form should show the existing data from that post.
    On form submission, update the post in the database and redirect to the user's page.
    """
    post = Feedback.query.get_or_404(post_id)
    username = post.user.username
    if 'username' in session and session['username'] == username:
        form = FeedbackForm(obj=post)
        if form.validate_on_submit():
            post.edit(title=form.title.data, content=form.content.data)
            flash('Feedback updated.')
            return redirect(f'/users/{username}')
        else:
            return render_template('edit-feedback.html', form=form, username=username)
    else:
        flash("You are not authorized to edit that feedback.")
        return redirect(f'/users/{username}')

@app.route('/feedback/<int:post_id>/delete', methods=['POST'])
def delete_feedback(post_id):
    """
    If the user is logged in with the username associated with the post in the route, delete the post and redirect back to the user's page.
    """
    post = Feedback.query.get_or_404(post_id)
    username = post.user.username
    if 'username' in session and session['username'] == username:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.')
    else:
        flash('You are not authorized to delete that post.')
    
    return redirect(f'/users/{username}')