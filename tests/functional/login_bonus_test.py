def test_on_login_bonus_is_received(test_client, user):
    assert user.real_money_wallet is None
    assert user.bonus_moneys == []

    response = test_client.post('/auth/login',
                                data=dict(username=user.username, password='asdf'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money_wallet is None
    assert len(user.bonus_moneys) == 1
    assert user.bonus_moneys[0].balance == 100

def test_on_login_bonus_is_received_multiple_times(test_client, user):
    assert user.real_money_wallet is None

    response = test_client.post('/auth/login',
                                data=dict(username=user.username, password='asdf'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money_wallet is None
    assert len(user.bonus_moneys) == 2
    assert user.bonus_moneys[1].balance == 100

    response = test_client.post('/auth/login',
                                data=dict(username=user.username, password='asdf'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert user.real_money_wallet is None
    assert len(user.bonus_moneys) == 3
    assert user.bonus_moneys[2].balance == 100