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