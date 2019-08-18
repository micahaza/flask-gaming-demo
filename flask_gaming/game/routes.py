from . import game
from flask import render_template

@game.route('/home')
def index():
    return render_template('home.html')

@game.route('/place-bet')
def place_bet():
    return render_template('place-a-bet.html')

