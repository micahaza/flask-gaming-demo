
def test_form_loads(test_client):
    response = test_client.get('/registration/')
    assert response.status_code == 200
    assert b"Create Account" in response.data
    assert b"Log In" in response.data
