from flask_gaming.models import RealMoneyWallet, BonusMoneyWallet, User


def test_can_create_user(app):
    u = User('asdfg', 'adsfg@asdfg.hu', 'adsfg')
    u.save()
    assert u.username == 'asdfg'


def test_can_set_user_real_money_balance(app, user):
    assert user.real_money_wallet is None
    user.real_money_wallet = RealMoneyWallet(100)
    user.save()
    assert user.real_money_wallet.balance == 100


def test_can_set_user_bonus_money_balance(app, user):
    assert user.bonus_money_wallets == []
    bm = BonusMoneyWallet(100)
    user.bonus_money_wallets.append(bm)
    user.save()
    assert user.bonus_money_wallets[0].balance == 100
