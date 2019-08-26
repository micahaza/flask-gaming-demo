from . import auth
from flask import request, render_template, redirect, session, url_for, current_app
from flask_gaming.models import User
from flask_gaming import bcrypt
from flask_gaming.cashier import Cashier
from flask_gaming.helpers import login_required


@auth.route('/')
def index():
    return 'Home...'


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_user = User.query.filter_by(username=username).first()
        if login_user is not None:
            if bcrypt.check_password_hash(login_user.password_hash, password) is True:
                session['logged_in'] = True
                session['username'] = login_user.username
                session['user_id'] = login_user.id
                cashier = Cashier(current_app.config)
                cashier.login_bonus(login_user)
                return redirect(url_for('game.index'))
        return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('auth.login'))
