from . import payment
from flask import render_template

@payment.route('/deposit', methods=('GET', 'POST'))
def deposit():
    return render_template('deposit.html')

@payment.route('/withdraw', methods=('GET', 'POST'))
def withdraw():
    return render_template('withdraw.html')

