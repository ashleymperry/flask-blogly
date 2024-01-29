"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, Users, default_image_url, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
import pdb

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = '$Boy07032018'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def go_to_users():
    return redirect('/users')

@app.route('/users')
def get_users():
    users = Users.query.all()
    return render_template('root.html', users=users)

@app.route('/users/new')
def get_add_user_page():
    return render_template('new-user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    image_url = image_url if image_url else default_image_url

    new_user = Users(first_name=first_name, last_name = last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    flash("User added!")

    return redirect('/users')

@app.route('/users/<int:user_id>')
def display_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_edit(user_id):
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    image_url = image_url if image_url else default_image_url

    user = Users.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    return render_template('new-post.html', user_id=user_id)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_post_edit(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/tags')
def get_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def get_tag_detail(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag-detail.html', tag=tag)

@app.route('/tags/new')
def create_new_tag():
    posts = Post.query.all()
    return render_template('new-tag.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    try:
        tag_name = request.form['tag-name']
        tag_post_ids = request.form.getlist('posts')
        tag = Tag(name=tag_name)
        posts = []
        for post_id in tag_post_ids:
            post = Post.query.get(int(post_id))
            posts.append(post)
        tag.posts = posts
        db.session.add(tag)
        db.session.commit()
    except Exception as err:
        print(err)
        return redirect('/tags/new')
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def get_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit-tag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    try:
        tag = Tag.query.get(tag_id)
        new_name = request.form['tag-name']
        tag_post_ids = request.form.getlist('posts')
        posts = []
        for post_id in tag_post_ids:
            post = Post.query.get(int(post_id))
            posts.append(post)
        tag.name = new_name
        tag.posts = posts
        db.session.commit()
    except Exception as err:
        print(err)
        return redirect(f'/tags/{tag_id}/edit')
        
    return redirect('/tags')
    
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')