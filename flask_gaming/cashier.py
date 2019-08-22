from . import db
from flask_gaming.models import RealMoneyWallet, BonusMoneyWallet
from flask_gaming import config

from .game_play import NotEnoughMoneyException

class Cashier(object):
    """
    Cashier manages user money, bonuses and restrictions.
    """
    def __init__(self, config):
        self.config = config

    def deposit(self, user, amount):
        if user.real_money is not None:
            user.real_money.balance += amount
        else:
            user.real_money = RealMoneyWallet(amount)
        user.save()
        self.__deposit_bonus(user, amount)

    def withdraw(self, user, amount):
        if user.real_money is not None and user.real_money.balance >= amount:
            user.real_money.balance -= amount
            user.save()
        else:
            raise NotEnoughMoneyException("User has not enough money to withdraw")

    def login_bonus(self, user):
        bm = BonusMoneyWallet(self.config['LOGIN_BONUS'])
        user.bonus_moneys.append(bm) 
        user.save()

    def __deposit_bonus(self, user, amount):
        if amount > 100:
            bm = BonusMoneyWallet(self.config['DEPOSIT_BONUS'])
            user.bonus_moneys.append(bm)
            user.save()
