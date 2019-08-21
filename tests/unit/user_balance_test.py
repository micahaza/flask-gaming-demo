from flask_gaming.models import RealMoney, BonusMoney, User

def test_can_create_user(app):
    u = User('asdfg', 'adsfg@asdfg.hu', 'adsfg')
    u.save()
    assert u.username == 'asdfg'

def test_can_set_user_real_money_balance(app, user):
    assert user.real_money == None
    user.real_money = RealMoney(100)
    user.save()
    assert user.real_money.balance == 100

def test_can_set_user_bonus_money_balance(app, user):
    assert user.bonus_money == None
    user.bonus_money = BonusMoney(100)
    user.save()
    assert user.bonus_money.balance == 100

