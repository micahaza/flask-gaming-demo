from . import payment
from flask import render_template, request, session
from flask_gaming.helpers import login_required
from flask_gaming.cashier import Cashier
from flask_gaming.models import User
from flask import current_app as app

@payment.route('/deposit', methods=('GET', 'POST'))
@login_required
def deposit():
    if request.method == "GET":
        return render_template('deposit.html')
    if request.method == "POST":
        user = User.query.get(session['user_id'])
        print(user)
        cashier = Cashier(app.config)
        cashier.deposit(user, float(request.form['amount'])) 
        return render_template('deposit.html')

@payment.route('/withdraw', methods=('GET', 'POST'))
@login_required
def withdraw():
    return render_template('withdraw.html')

