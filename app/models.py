from datetime import datetime
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from hashlib import md5
from time import time
import jwt

# Followers table to support self-referential many-to-many
# users followers/followed
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# Inherits from db.Model, a base class for all SQLAlchemy modules
# Fiels variables are instances of db.Column class
class User(UserMixin, db.Model):
    # id is our primary key
    id = db.Column(db.Integer, primary_key=True)
    # limit this column to 64 characters
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    # Added for Chapter 6 to add decoration to user profile
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

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
    
    # Define how to view an avatar for each user
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
    # Follow a user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    # Unfollow a user
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # Check if we're following a user
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    # Get posts from followed users and self
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
    # Generate password reset token
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password' : self.id, 'exp' : time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # Verify password reset token
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

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