from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Something something login
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    # Render login form
    return render_template('login.html', title='Sign In', form=form)