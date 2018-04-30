from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse # TODO: Continue Chapter 5 from here

# Default/index page. This page requires user login
@app.route('/')
@app.route('/index')
@login_required
def index():
    # Dummy username and posts
    user = {'username': 'Andrew'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

# Old login route. Superseded by new one using Flask-Login
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    form = LoginForm()
#
#    # Something something login
#    if form.validate_on_submit():
#        flash('Login requested for user {}, remember_me={}'.format(
#            form.username.data, form.remember_me.data))
#        return redirect(url_for('index'))
#
#    # Render login form
#    return render_template('login.html', title='Sign In', form=form)

# Log user out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))