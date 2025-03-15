from flask import *
from flask_login import current_user
from models import User, File
from extensions import db
import os


def _change_profile(user_id, type):
    user = User.query.get_or_404(user_id)
    if not current_user.is_admin and user != current_user:
        return redirect(url_for('no_permission'))
    if type == "image":
        if request.method == 'POST':
            file = request.files['file']
            if file:
                nxt = file.filename.split('.')[-1]
                file.filename=str(user_id)+'.'+nxt
                user.image_file = file.filename
                db.session.commit()
                for f in os.listdir("static/images/user"):
                    if f.startswith(str(user_id)):
                        os.remove("static/images/user/"+f)
                file.save(os.path.join("static/images/user", file.filename))
                flash('Profile picture changed successfully!', 'success')
                return redirect(url_for('profile_show', user_id=user.id))
        if request.method == 'GET':
            return render_template('change_profile.html', user=user, type="image")

def _profile_show():
    user = current_user
    return render_template('profile_show.html', user=user, files=File.query.filter_by(user_id=current_user.id).all())
