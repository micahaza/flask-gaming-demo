from flask_gaming.models import User, Bet, Win, RealMoney, BonusMoney

class NotEnoughMoneyException(Exception):
    def __init__(self, message):
        self.message = message

class GamePlay(object):

    def __init__(self, config):
        self.config = config

    def spin(self, user):
        if user.real_money is not None and user.real_money.balance >= self.config['BET_AMOUNT']:
            pass
        # elif user.bonus_money[0].balance >= self.config['BET_AMOUNT']:
        #     pass
        else:
            raise NotEnoughMoneyException("User has not enough money to play")
