import pytest
from flask_gaming import create_app, db, bcrypt
from flask_gaming.models import User
from flask import session, request

@pytest.fixture(scope='module')
def new_user():
    user = User('deezent', 'deezent@gmail.com', bcrypt.generate_password_hash('asdf'))
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing.cfg')
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    app = create_app('testing.cfg')
    db.create_all()

    # Insert user data
    user = User('deezent', 'deezent@gmail.com', bcrypt.generate_password_hash('asdf'))
    db.session.add(user)

    # Commit the changes for the users
    db.session.commit()

    # this is where the testing happens!
    yield db

    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='function')
def logged_in_client():
    app = create_app('testing.cfg')
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['username'] = 'deezent'
        yield client