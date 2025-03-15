from flask import *
from flask_login import login_required, current_user
from models import Post, File

def _search():
    query = request.args.get('query')
    if current_user.is_authenticated:
        user_post = Post.query.filter_by(user_id=current_user.id).all()
        user_files = File.query.filter_by(user_id=current_user.id).all()
    else:
        user_post = []
        user_files = []
    if query:
        posts = Post.query.filter(Post.title.like(f'%{query}%')).all()
        posts2 = Post.query.filter(Post.topic.like(f'%{query}%')).all()
        posts = list(set(posts) | set(posts2))
    else:
        posts = Post.query.all()
    return render_template('index.html', posts=posts, query=query, user_post=user_post, user_files=user_files)

def _home():
    posts = Post.query.all()
    if current_user.is_authenticated:
        user_post = Post.query.filter_by(user_id=current_user.id).all()
        user_files = File.query.filter_by(user_id=current_user.id).all()
    else:
        user_post = []
        user_files = []
    return render_template('index.html', posts=posts, user_post=user_post, user_files=user_files)