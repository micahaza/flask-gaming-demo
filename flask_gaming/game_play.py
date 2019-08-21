from flask_gaming.models import User, Bet, Win, RealMoney, BonusMoney
# from flask import current_app
import random


class NotEnoughMoneyException(Exception):
    def __init__(self, message):
        self.message = message

class GamePlay(object):

    def __init__(self, config):
        self.config = config

    def spin(self, user):
        if user.real_money is not None and user.real_money.balance >= self.config['BET_AMOUNT']:
            bet = Bet(self.config['BET_AMOUNT'])
            win = Win(random.choice([0, 1])* 4)
            user.real_money.balance -= self.config['BET_AMOUNT']
            user.bets.append(bet)
            user.wins.append(win)
            user.real_money.balance += win.amount
            user.save()
        elif user.bonus_money_sum >= self.config['BET_AMOUNT']:
            pass
        else:
            raise NotEnoughMoneyException("User has not enough money to play")
