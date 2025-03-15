from datetime import datetime

from flask import *
from flask_login import login_required, current_user
from markupsafe import Markup

from models import Post, Comment, File
from extensions import db
import markdown

def _new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        topic = request.form['topic'].strip(' ')
        post = Post(title=title, content=content, author=current_user, topic=topic)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('post.html')

def _view_post(post_id):
    if request.method == 'GET':
        post = Post.query.get_or_404(post_id)
        exts = ["codehilite", "nl2br", "fenced_code", "tables", "sane_lists", "admonition", "attr_list", "def_list", "footnotes", "meta", "smarty", "toc", "wikilinks", "mdx_math"]
        md = markdown.Markdown(extensions=exts, extension_configs={
            'mdx_math': {
                'enable_dollar_delimiter': True,  # 是否启用单美元符号（默认只启用双美元）
                'add_preview': True  # 在公式加载成功前是否启用预览（默认不启用）
            }
        })
        return render_template('view_post.html', post=post, content=Markup(md.convert(post.content)), comments=Comment.query.filter_by(post_id=post.id).all())
    if request.method == 'POST':
        return redirect(url_for('comment', post_id=post_id))

def _delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()
    if not current_user.is_admin and post.author != current_user:
        return redirect(url_for('no_permission'))
    db.session.delete(post)
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()
    file = open("./log", "w+")
    file.write("Post " + post.title + " deleted by " + current_user.username + " at " + str(datetime.now()) + "\n")
    file.close()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('home'))

def _edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not current_user.is_admin and post.author != current_user:
        return redirect(url_for('no_permission'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.topic = request.form['topic']
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('view_post', post_id=post.id))

    return render_template('edit_post.html', post=post)