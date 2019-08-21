from . import db
from flask_gaming.models import RealMoney, BonusMoney
from flask_gaming import config

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
            user.real_money = RealMoney(amount)
        user.save()
        self.__deposit_bonus(user, amount)

    def withdraw(self, user, amount):
        pass

    def login_bonus(self, user):
        user.bonus_money = BonusMoney(self.config['LOGIN_BONUS'], user=user)
        user.save()

    def __deposit_bonus(self, user, amount):
        if amount > 100:
            bm = BonusMoney(self.config['DEPOSIT_BONUS'])
            user.bonus_moneys.append(bm)
            user.save()
