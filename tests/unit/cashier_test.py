from flask_gaming.models import User
from flask_gaming.cashier import Cashier

def test_can_create_cashier(app, cashier):
    assert cashier is not None

def test_cashier_deposit(app, user, cashier):
    assert user is not None
    assert user.real_money is None
    assert user.bonus_money is None
    cashier.deposit(user, 15)
    assert user.real_money.balance == 15

def test_cashier_bonus_less_than_100_or_equal_deposit(app, user, cashier):
    cashier.deposit(user, 10)
    assert user.real_money.balance == 25
    assert user.bonus_money is None
    cashier.deposit(user, 99)
    assert user.real_money.balance == 124
    assert user.bonus_money is None
    cashier.deposit(user, 100)
    assert user.real_money.balance == 224
    assert user.bonus_money is None

def test_cashier_bonus_more_than_100_deposit(app, user, cashier):
    old_balance = user.real_money.balance
    cashier.deposit(user, 200)
    assert user.real_money.balance == old_balance + 200
    assert user.bonus_money.balance == 20

def test_cashier_login_bonus(app):
    assert True