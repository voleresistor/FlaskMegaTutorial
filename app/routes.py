from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

# Perform actions before every request
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # Flask-Login auto-invokes current user load so only commit is needed
        db.session.commit()

# Default/index page. This page requires user login
@app.route('/')
@app.route('/index')
@login_required
def index():
    # Dummy posts
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in my butt!'
        },
        {
            'author': {'username': 'Cynthia'},
            'body': 'The Avengers movie was formulaic and dull'
        }
    ]

    # Render index page
    return render_template('index.html', title='Home', posts=posts) #user=current_user, 

# Flask-Login supported user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect user to home page if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # .first() return user object or None
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # Handle redirecting back to previous page after a login
        # if next_page wasn't provided or netloc includes a domain
        # redirect to index. This ensures that URLs are always
        # relative for security purposes
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

# Log user out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User profile page
# .first_or_404() automatically returns a 404 error
# if requested user doesn't exist
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post 1'},
        {'author': user, 'body': 'Test post 2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# Allow user to edit their profile
# return statement lives outside elif to handle invalid POST as
# well as fresh GET
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)