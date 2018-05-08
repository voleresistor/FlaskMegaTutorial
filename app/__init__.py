from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
import logging, os

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

# Handle sending emails to users
# start mail server emulation with
# python3 -m smtpd -n -c DebuggingServer localhost:8025
# Add env vars
# export MAIL_SERVER=localhost
# export MAIL_PORT=8025
mail = Mail(app)

# Handle errors
if not app.debug:
    # Send email on error
    # Severity ERROR
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
            toaddrs = app.config['ADMINS'],
            subject = 'Microblog Failure',
            credentials = auth,
            secure = secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # Write error logs
    # Severity INFO or higher
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=30)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

# This reference's location avoids circular imports since routes will
# import the app object created in this file
# app is the app created by __init__.py in this command
# the name app is taken from the folder name
# models defines database structure
from app import routes, models, errors