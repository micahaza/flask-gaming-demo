from flask_gaming.models import User, Bet, Win, BonusMoneyWallet
# from flask import current_app
import random


class NotEnoughMoneyException(Exception):
    def __init__(self, message):
        self.message = message

class GamePlay(object):

    def __init__(self, config):
        self.config = config

    def spin(self, user):
        # real money used first
        if user.real_money is not None and user.real_money.balance >= self.config['BET_AMOUNT']:
            bet = Bet(self.config['BET_AMOUNT'], amount_type='real')
            win = Win(random.choice([0, 0, 1])* 4, amount_type='real')
            user.real_money.balance -= self.config['BET_AMOUNT']
            user.bets.append(bet)
            user.wins.append(win)
            user.real_money.balance += win.amount
            user.save()
        elif user.bonus_money_sum >= self.config['BET_AMOUNT']:
            for bw in user.bonus_moneys:
                rng = random.choice([0, 0, 1])* 4
                if bw.balance >= self.config['BET_AMOUNT']:
                    bw.balance -= self.config['BET_AMOUNT']
                    bet = Bet(self.config['BET_AMOUNT'], amount_type='bonus', bonus_wallet_id = bw.id)
                    win = Win(rng, amount_type='bonus', bonus_wallet_id = bw.id)
                    if rng > 0:
                        bw.balance += rng
                    user.bets.append(bet)
                    user.wins.append(win)
            user.save()
        else:
            raise NotEnoughMoneyException("User has not enough money to play")
