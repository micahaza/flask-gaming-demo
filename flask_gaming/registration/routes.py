from . import registration
from flask import request, render_template, redirect, url_for
from flask_gaming.models import User
from flask_gaming import bcrypt


@registration.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        u_exists = User.query.filter_by(username=username).first()
        if u_exists is not None:
            return redirect(url_for('registration.index'))
        else:
            u = User()
            u.username = username
            u.email = email
            u.password_hash = bcrypt.generate_password_hash(password)
            u.save()
    return redirect(url_for('auth.login'))
