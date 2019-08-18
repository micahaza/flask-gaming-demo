from . import game
from flask import render_template
from flask_gaming.helpers import login_required

@game.route('/home')
@login_required
def index():
    return render_template('home.html')

@game.route('/place-bet')
@login_required
def place_bet():
    return render_template('place-a-bet.html')

