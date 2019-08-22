import pytest
from flask_gaming.models import RealMoneyWallet, User
from flask_gaming.game_play import NotEnoughMoneyException

def test_page_loads(logged_in_client, user):
    rv = logged_in_client.get('/payment/withdraw')
    assert b'Withdraw' in rv.data
    assert rv.status_code == 200

def test_can_withdraw10(logged_in_client, user):
    user.real_money = RealMoneyWallet(10)
    user.save()
    response = logged_in_client.post('/payment/withdraw',
                data=dict(amount=10),
                follow_redirects=True)
    assert response.status_code == 200
    updated_user = User.query.get(user.id)
    assert updated_user.real_money.balance == 0

def test_can_not_withdraw_if_has_not_enough_money(logged_in_client, user):
    with pytest.raises(NotEnoughMoneyException):
        response = logged_in_client.post('/payment/withdraw',
                data=dict(amount=10),
                follow_redirects=True)
        assert response.status_code == 200
        assert user.real_money.balance == 0
        assert user.real_money.balance == 0

