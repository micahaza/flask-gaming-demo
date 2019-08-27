def test_can_create_cashier(app, cashier):
    assert cashier is not None


def test_cashier_deposit(app, user, cashier):
    assert user is not None
    assert user.real_money_wallet is None
    assert user.bonus_money_wallets == []
    cashier.deposit(user, 15)
    assert user.real_money_wallet.balance == 15


def test_cashier_bonus_less_than_100_or_equal_deposit(app, user, cashier):
    cashier.deposit(user, 10)
    assert user.real_money_wallet.balance == 25
    assert user.bonus_money_wallets == []
    cashier.deposit(user, 99)
    assert user.real_money_wallet.balance == 124
    assert user.bonus_money_wallets == []
    cashier.deposit(user, 100)
    assert user.real_money_wallet.balance == 224
    assert user.bonus_money_wallets == []


def test_cashier_bonus_more_than_100_deposit(app, user, cashier):
    old_balance = user.real_money_wallet.balance
    cashier.deposit(user, 200)
    assert user.real_money_wallet.balance == old_balance + 200
    assert user.bonus_money_wallets[0].balance == 20
