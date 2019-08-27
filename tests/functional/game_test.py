import pytest
from flask_gaming.game_play import NotEnoughMoneyException
from flask_gaming.models import BonusMoneyWallet, User


def test_page_loads(logged_in_client):
    response = logged_in_client.get('/game/place-bet')
    assert response.status_code == 200


def test_no_balance_bet(logged_in_client, user):
    assert user.real_money_wallet is None
    assert len(user.bonus_money_wallets) == 0

    with pytest.raises(NotEnoughMoneyException):
        response = logged_in_client.post('/game/place-bet')
        assert response.status_code == 200

    assert user.real_money_wallet is None
    assert len(user.bonus_money_wallets) == 0


def test_bet_if_user_has_real_money_only(logged_in_client, user, cashier, app):
    cashier.deposit(user, 100)
    assert user.real_money_wallet.balance == 100
    logged_in_client.post('/game/place-bet')
    assert user.real_money_wallet.balance in [100 - app.config['BET_AMOUNT'], 102]
    assert user.bets[0].amount == app.config['BET_AMOUNT']
    assert user.wins[0].amount in [0, 4]
    assert len(user.bonus_money_wallets) == 0
    assert len(user.bets) == 1
    assert len(user.wins) == 1


def test_when_bonus_money_is_not_enough_to_bet(logged_in_client, user):
    user.real_money_wallet.balance = 0
    bm = BonusMoneyWallet(1)
    user.bonus_money_wallets.append(bm)
    user.save()
    assert user.real_money_wallet.balance == 0
    assert len(user.bonus_money_wallets) == 1
    assert user.bonus_money_wallets[0].balance == 1

    with pytest.raises(NotEnoughMoneyException):
        response = logged_in_client.post('/game/place-bet')
        assert response.status_code == 200
        assert user.real_money_wallet.balance == 0
        assert len(user.bonus_money_wallets) == 1
        assert user.bonus_money_wallets[0].balance == 1


def test_real_money_used_first(logged_in_client, user, app):
    user.real_money_wallet.balance = 100
    bm = BonusMoneyWallet(20)
    user.bonus_money_wallets.append(bm)
    user.save()

    logged_in_client.post('/game/place-bet')
    assert user.real_money_wallet.balance in [100 - app.config['BET_AMOUNT'], 102]
    assert user.bonus_money_wallets[0].balance == 1
    assert user.bonus_money_wallets[1].balance == 20


def test_bonus_money_is_used_when_real_money_balance_is_not_enough(logged_in_client, user, app):
    user.real_money_wallet.balance = 0
    user.save()
    assert user.real_money_wallet.balance == 0
    assert user.bonus_money_sum == 21
    logged_in_client.post('/game/place-bet')
    updated_user = User.query.get(user.id)
    assert updated_user.real_money_wallet.balance == 0
    assert updated_user.bonus_money_sum in [18, 22]


def test_bonus_money_is_used_correcly(logged_in_client, user, testdb):
    user.real_money_wallet.balance = 0
    user.save()
    assert user.real_money_wallet.balance == 0
    testdb.engine.execute("delete from bets")
    testdb.engine.execute("delete from wins")
    testdb.engine.execute("delete from bonus_money_wallets")
    testdb.session.commit()

    # add three 1 euro bonus money to user
    bm = BonusMoneyWallet(1)
    user.bonus_money_wallets.append(bm)
    bm = BonusMoneyWallet(1)
    user.bonus_money_wallets.append(bm)
    bm = BonusMoneyWallet(10)
    user.bonus_money_wallets.append(bm)
    user.save()
    # spin
    logged_in_client.post('/game/place-bet')
    assert user.real_money_wallet.balance == 0
    assert user.bonus_money_sum in [8, 12]


def test_if_real_money_used_win_will_return_to_the_real_money_wallet(logged_in_client, user):
    user.real_money_wallet.balance = 20
    user.save()
    logged_in_client.post('/game/place-bet')
    assert user.real_money_wallet.balance in [18, 22]


def test_bonus_money_wins_return_to_the_correct_wallet(logged_in_client, user, testdb):
    testdb.engine.execute("delete from bets")
    testdb.engine.execute("delete from wins")
    testdb.engine.execute("delete from bonus_money_wallets")
    testdb.session.commit()

    user.real_money_wallet.balance = 0
    bm = BonusMoneyWallet(1)
    user.bonus_money_wallets.append(bm)
    bm2 = BonusMoneyWallet(10)
    user.bonus_money_wallets.append(bm2)
    user.save()
    assert user.real_money_wallet.balance == 0
    assert user.bonus_money_sum == 11
    logged_in_client.post('/game/place-bet')
    assert user.real_money_wallet.balance == 0
    assert bm2.balance in [8, 12]
