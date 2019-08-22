from flask_gaming.models import Bet

def test_cash_in_possible_property(user, testdb, cashier, app):
    cashier.login_bonus(user)
    bmw = user.bonus_moneys[0]
    assert bmw.cash_in_possible == False
    steps = app.config['WAGERING_REQUIREMENT'] * app.config['LOGIN_BONUS'] / app.config['BET_AMOUNT']
    for idx in range(int(steps)):
        bet = Bet(app.config['BET_AMOUNT'], amount_type='bonus', bonus_money_wallet_id = bmw.id)
        user.bets.append(bet)
    user.save()

    assert bmw.cash_in_possible == True
