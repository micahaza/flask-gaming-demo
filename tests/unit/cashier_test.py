from flask_gaming.cashier import Cashier
from flask_gaming.models import User

def test_class_creates(test_client):
    c = Cashier()
    assert c is not None

def test_user_initial_balance_is_zero(init_database):
    c = Cashier()
    u = User.query.filter_by(username='deezent').first()
    assert u.real_money_balance() == 0
    assert u.bonus_money_balance() == 0
