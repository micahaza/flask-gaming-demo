import pytest
from flask_gaming.game_play import NotEnoughMoneyException

def test_not_enough_money(user, game):
    with pytest.raises(NotEnoughMoneyException):
        assert game.spin(user)
