def test_page_loads(logged_in_client):
    rv = logged_in_client.get('/payment/deposit')
    assert b'Deposit' in rv.data
    assert rv.status_code == 200


def test_1_deposit(logged_in_client, user):
    assert user.real_money_wallet is None
    assert user.bonus_money_wallets == []

    response = logged_in_client.post('/payment/deposit', data=dict(amount=1))
    assert response.status_code == 200
    assert user.real_money_wallet.balance == 1


def test_100(logged_in_client, user):
    assert user.bonus_money_wallets == []
    response = logged_in_client.post('/payment/deposit', data=dict(amount=100))
    assert response.status_code == 200
    assert user.real_money_wallet.balance == 101
    assert user.bonus_money_wallets == []


def test_120_deposit_bonus_received(logged_in_client, user):
    assert user.bonus_money_wallets == []
    response = logged_in_client.post('/payment/deposit', data=dict(amount=120))
    assert response.status_code == 200
    assert user.real_money_wallet.balance == 221
    assert user.bonus_money_wallets[0].balance == 20


def test_60_60_deposit_bonus_not_received(logged_in_client, user):
    assert len(user.bonus_money_wallets) == 1
    response = logged_in_client.post('/payment/deposit', data=dict(amount=60))
    assert response.status_code == 200
    assert user.real_money_wallet.balance == 281
    assert len(user.bonus_money_wallets) == 1

    response = logged_in_client.post('/payment/deposit', data=dict(amount=60))
    assert response.status_code == 200
    assert user.real_money_wallet.balance == 341
    assert len(user.bonus_money_wallets) == 1


def test_200_200_bonus_money_received(logged_in_client, user):
    assert len(user.bonus_money_wallets) == 1
    response = logged_in_client.post('/payment/deposit', data=dict(amount=200))
    assert response.status_code == 200
    assert user.real_money_wallet.balance == 541
    assert len(user.bonus_money_wallets) == 2

    response = logged_in_client.post('/payment/deposit', data=dict(amount=200))
    assert response.status_code == 200
    assert user.real_money_wallet.balance == 741
    assert len(user.bonus_money_wallets) == 3
    assert user.bonus_money_wallets[0].balance == 20
    assert user.bonus_money_wallets[1].balance == 20
    assert user.bonus_money_wallets[2].balance == 20
