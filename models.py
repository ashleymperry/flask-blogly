"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime

default_image_url = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class Users(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        return f'<id: {self.id} first_name: {self.first_name} last_name: {self.last_name}>'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False, default=default_image_url)

    posts = db.relationship('Post', backref='user', single_parent=True, cascade='all, delete')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Tag(db.Model):
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), unique=True)
    
    posts = db.relationship('Post', secondary='post_tags', backref='tags')
    
class PostTag(db.Model):
    __tablename__ = "post_tags"
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    
    