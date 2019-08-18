# from flask.models import User

def test_new_user(new_user):
    assert new_user.email == 'deezent@gmail.com'
    assert new_user.username == 'deezent1'