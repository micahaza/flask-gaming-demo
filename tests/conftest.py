import pytest
from flask_gaming import create_app, db, bcrypt
from flask_gaming.models import User
from flask import session
from flask_gaming.cashier import Cashier

@pytest.fixture(scope='module')
def app():
    app = create_app('testing.cfg')
    with app.app_context():   
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(app):
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

@pytest.fixture(scope='module')
def cashier(app):
    yield Cashier(app.config)

@pytest.fixture(scope='module')
def user(app):
    user = User('deezent', 'deezent@gmail.com', bcrypt.generate_password_hash('asdf'))
    db.session.add(user)
    db.session.commit()
    yield user

@pytest.fixture(scope='module')
def logged_in_client(app, user):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['username'] = user.username
            sess['user_id'] = user.id
        yield client
