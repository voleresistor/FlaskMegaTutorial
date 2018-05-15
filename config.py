import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SECRET_KEY protects against web exploits
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Get from DATABASE_URL environment variable. If that doesn't
    # exist, build path from basedir of app
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Don't notify app every time a database change occurs
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email error stacktraces to an administrator
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin1@example.com', 'admin2@example.com']

    # Handle pagination
    POSTS_PER_PAGE = 25

    # Add support for multiple languages using Flask-Babel
    LANGUAGES = ['en', 'es']