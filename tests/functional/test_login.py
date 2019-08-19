
def test_login_page_loads(test_client):
    rv = test_client.get('/auth/login')
    assert b'Login' in rv.data
    assert rv.status_code == 200

def test_login_with_wrong_credentials(test_client, init_database):
    response = test_client.post('/auth/login',
                                data=dict(username='asdff', password='asdf'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"asdff" not in response.data
    assert b"Logout" not in response.data
    assert b"Deposit" not in response.data
    assert b"Withdraw" not in response.data
    assert b"Login" in response.data
    assert b"Create one" in response.data

def test_login_with_good_credentials(test_client, new_user):
    response = test_client.post('/auth/login',
                                data=dict(username=new_user.username, password='asdf'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"deezent" in response.data
    assert b"Logout" in response.data
    assert b"Deposit" in response.data
    assert b"Withdraw" in response.data
    assert b"Login" not in response.data
    assert b"Create one" not in response.data

def test_protected_page_access(logged_in_client):
    response = logged_in_client.get('/game/home')
    assert response.status_code == 200
    assert b"deezent" in response.data