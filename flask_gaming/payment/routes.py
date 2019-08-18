from . import payment
from flask import render_template
from flask_gaming.helpers import login_required

@payment.route('/deposit', methods=('GET', 'POST'))
@login_required
def deposit():
    return render_template('deposit.html')

@payment.route('/withdraw', methods=('GET', 'POST'))
@login_required
def withdraw():
    return render_template('withdraw.html')

