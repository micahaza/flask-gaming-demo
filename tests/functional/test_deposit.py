def test_page_loads(logged_in_client):
    rv = logged_in_client.get('/payment/deposit')
    assert b'Deposit' in rv.data
    assert rv.status_code == 200

def test_1_deposit(logged_in_client):
    response = logged_in_client.post('/payment/deposit',
                data=dict(amount=1),
                follow_redirects=True)
    assert response.status_code == 200

def test_100(logged_in_client):
    pass

def test_120(logged_in_client):
    pass

def test_50_50(logged_in_client):
    pass

def test_200(logged_in_client):
    pass
