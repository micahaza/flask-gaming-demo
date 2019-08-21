# from flask_gaming.models import RealMoney, BonusMoney

def test_page_loads(logged_in_client):
    response = logged_in_client.get('/game/place-bet')
    assert response.status_code == 200

def test_no_balance_bet(logged_in_client, user):
    assert user.real_money is None
    assert len(user.bonus_moneys) == 0
    response = logged_in_client.post('/game/place-bet')
    assert response.status_code == 200
    assert user.real_money is None
    assert len(user.bonus_moneys) == 0

def test_bet_if_user_has_real_money_only(logged_in_client, user, cashier):
    cashier.deposit(user, 100)
    assert user.real_money.balance == 100
    response = logged_in_client.post('/game/place-bet')

# def test_real_and_bonus_money(test_client):
#     pass

# def test_real_money_used_first(test_client):
#     pass
