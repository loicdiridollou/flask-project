from application import application

def test_home():
    response = application.test_client().get('/')

    assert response.status_code == 200
