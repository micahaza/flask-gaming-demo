import pytest
from flask_gaming import create_app, db, bcrypt
from flask_gaming.models import User

@pytest.fixture(scope='module')
def new_user():
    user = User('deezent1', 'deezent@gmail.com', bcrypt.generate_password_hash('asdf'))
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
    # Create the database and the database table
    app = create_app('testing.cfg')
    db.create_all()
    
    # Insert user data
    user1 = User('deezent1', 'deezent1@gmail.com', bcrypt.generate_password_hash('asdf'))
    user2 = User('deezent2', 'deezent2@gmail.com', bcrypt.generate_password_hash('asdf'))
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    with app.app_context():
        db.drop_all()
