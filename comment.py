from datetime import datetime

from flask import request, redirect, url_for, flash
from flask_login import current_user

from extensions import db
from models import Post, Comment


def _comment(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.add(Comment(content=request.form.get("content"), post_id=post.id, auther=current_user))
    db.session.commit()
    return redirect(url_for('view_post', post_id=post.id))

def _delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not current_user.is_admin and comment.auther != current_user:
        return redirect(url_for('no_permission'))
    db.session.delete(comment)
    db.session.commit()
    file = open("./log", "w+")
    file.write("Comment " + comment.content + " deleted by " + current_user.username + " at " + str(datetime.now()) + "\n")
    file.close()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('view_post', post_id=comment.post_id))