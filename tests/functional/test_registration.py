
def test_form_loads(test_client):
    response = test_client.get('/registration/')
    assert response.status_code == 200
    assert b"Create Account" in response.data
    assert b"Log In" in response.data

def test_empty_submit(test_client):
    pass

def test_valid_data(test_client, init_database):
    pass

def test_invalid_data(test_client):
    pass

def test_double_registration(test_client, init_database):
    pass
