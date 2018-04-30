from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Inherits from db.Model, a base class for all SQLAlchemy modules
# Fiels variables are instances of db.Column class
class User(UserMixin, db.Model):
    # id is our primary key
    id = db.Column(db.Integer, primary_key=True)
    # limit this column to 64 characters
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Create one-to-many relationship to new Post object
    # Referenced by string containing class name (if class is defined in this file)
    # backref creates a field added to objects from "many" side
    # lazy defines how the query is issued
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Useful for debugging: Tells Py by to print these objects
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Set user password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Compare password to password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # We're building Twitter, I guess?
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Reference to id value from User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Implement user loader to support Flask-Login
# @login.user_loader decorator registers this function with Flask-Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))