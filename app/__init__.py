from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# app here is an instance of Flask
# this object is a member of the app package
app = Flask(__name__)
app.config.from_object(Config)

# Database
db = SQLAlchemy(app)

# Migration engine
migrate = Migrate(app, db)

# Initialize login manager
# Set redirect page when users navigate to protected pages
login = LoginManager(app)
login.login_view = 'login'

# This reference's location avoids circular imports since routes will
# import the app object created in this file
# app is the app created by __init__.py in this command
# the name app is taken from the folder name
# models defines database structure
from app import routes, models