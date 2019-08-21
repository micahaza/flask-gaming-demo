def test_page_loads(logged_in_client):
    rv = logged_in_client.get('/payment/deposit')
    assert b'Deposit' in rv.data
    assert rv.status_code == 200

def test_1_deposit(logged_in_client, user):
    assert user.real_money is None
    assert user.bonus_moneys == []

    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=1),
                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money.balance == 1

def test_100(logged_in_client, user):
    assert user.bonus_moneys == []
    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=100),
                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money.balance == 101
    assert user.bonus_moneys == []

def test_120_deposit_bonus_received(logged_in_client, user):
    assert user.bonus_moneys == []
    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=120),
                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money.balance == 221
    assert user.bonus_moneys[0].balance == 20

def test_60_60_deposit_bonus_not_received(logged_in_client, user):
    assert len(user.bonus_moneys) == 1
    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=60),
                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money.balance == 281
    assert len(user.bonus_moneys) == 1

    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=60),
                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money.balance == 341
    assert len(user.bonus_moneys) == 1

def test_200_200_bonus_money_received(logged_in_client, user):
    assert len(user.bonus_moneys) == 1
    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=200),
                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money.balance == 541
    assert len(user.bonus_moneys) == 2

    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=200),
                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money.balance == 741
    assert len(user.bonus_moneys) == 3

