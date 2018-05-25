from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler

# app here is an instance of Flask
# this object is a member of the app package
app = Flask(__name__)
app.config.from_object(Config)

# Database
db = SQLAlchemy()

# Migration engine
migrate = Migrate()

# Initialize login manager
# Set redirect page when users navigate to protected pages
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please login to access this page.'

# Handle sending emails to users
# start mail server emulation with
# python3 -m smtpd -n -c DebuggingServer localhost:8025
# Add env vars
# export MAIL_SERVER=localhost
# export MAIL_PORT=8025
mail = Mail()

# Flask-Bootstrap uses the Twitter css bootstrap files to
# make simple styling easier
bootstrap = Bootstrap()

# Flask-Moment helps with formatting dates and times to match
# the user's locale settings
moment = Moment()

# Create the application
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(db)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # Register errors Blueprint with main application
    # The import here avoids circular dependencies that may arise
    # if it's imported higher up in the code
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    # Register auth Blueprint with main application
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Register main Blueprint with main application
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Handle errors
    if not app.debug and not app.testing:
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
    
    return app