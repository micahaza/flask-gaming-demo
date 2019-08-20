from . import db
from run import app
from flask_gaming.models import RealMoney, BonusMoney

class Cashier(object):
    """
    Cashier manages user money, bonuses and restrictions.
    """
    def __init__(self):
        pass

    def deposit(self, user, amount):
        if user.real_money is not None:
            user.real_money.balance += amount
        else:
            user.real_money = RealMoney(amount)
        user.save()
        self.__deposit_bonus(user, amount)

    def withdraw(self, user, amount):
        pass

    def __login_bonus(self, user, amount):
        pass

    def __deposit_bonus(self, user, amount):
        if amount > 100 and user.bonus_money is None:
            user.bonus_money = BonusMoney(app.config['DEPOSIT_BONUS'])
            user.save()
