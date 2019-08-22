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
        
        bet = Bet(self.config['BET_AMOUNT'])
        win = Win(random.choice([0, 1])* 4)
        
        # real money used first
        if user.real_money is not None and user.real_money.balance >= self.config['BET_AMOUNT']:
            user.real_money.balance -= self.config['BET_AMOUNT']
            user.bets.append(bet)
            user.wins.append(win)
            user.real_money.balance += win.amount
            user.save()
        elif user.bonus_money_sum >= self.config['BET_AMOUNT']:
            remainder = self.config['BET_AMOUNT']
            while remainder > 0:
                for bm in user.bonus_moneys:
                    if bm.balance >= remainder:
                        bm.balance -= remainder
                        remainder = 0
                    else:
                        remainder -= bm.balance
                        bm.balance = 0
            user.save()
        else:
            raise NotEnoughMoneyException("User has not enough money to play")
