from datetime import datetime

from flask import *
from flask_login import current_user
from models import Post, User, File, Comment
from extensions import db

def _admin():
    if not current_user.is_admin:
        return redirect(url_for('no_permission'))
    users = User.query.all()
    posts = Post.query.all()
    files = File.query.all()
    return render_template('admin.html', users=users, posts=posts, files=files)

def _delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('no_permission'))
    if user_id == current_user.id:
        flash('You cannot delete yourself!', 'danger')
        return redirect(url_for('admin'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    file = open("./log", "w+")
    file.write("User " + user.username + " deleted by " + current_user.username + " at " + str(datetime.now()) + "\n")
    file.close()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin'))

def _make_admin(user_id):
    if not current_user.is_admin:
        return redirect(url_for('no_permission'))
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('User is already an admin!', 'danger')
        return redirect(url_for('admin'))
    user.is_admin = True
    db.session.commit()
    file = open("./log", "w+")
    file.write("User " + user.username + " made admin by " + current_user.username + " at " + str(datetime.now()) + "\n")
    file.close()
    flash("User made admin successfully!", 'success')
    return redirect(url_for('admin'))

def _remove_admin(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    if not user.is_admin:
        flash('User is not an admin!', 'danger')
        return redirect(url_for('admin'))
    if user.id == current_user.id:
        flash('You cannot remove yourself from admins!', 'danger')
        return redirect(url_for('admin'))
    user.is_admin = False
    db.session.commit()
    file = open("./log", "w+")
    file.write("User " + user.username + " remove from admin by " + current_user.username + " at " + str(datetime.now()) + "\n")
    file.close()
    flash("User removed from admin successfully!", 'success')
    return redirect(url_for('admin'))