from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from extensions import bcrypt, db
from models import *
def _register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User()
        user.username = username
        user.email = email
        user.password = hashed_password
        if User.query.filter_by(username=username).first() is None and User.query.filter_by(email=email).first() is None:
            db.session.add(user)
            db.session.commit()
        else:
            flash('Username or email already exists!', 'danger')
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

def _login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

def _logout():
    logout_user()
    return redirect(url_for('home'))