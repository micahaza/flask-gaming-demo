from . import game
from flask import render_template, request, session
from flask_gaming.helpers import login_required
from flask_gaming.models import User

@game.route('/home')
@login_required
def index():
    return render_template('home.html')

@game.route('/place-bet', methods=['GET', 'POST'])
@login_required
def place_bet():
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        # print(user)
    return render_template('place-a-bet.html')

