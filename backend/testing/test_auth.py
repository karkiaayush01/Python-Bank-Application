from fastapi.testclient import TestClient
from ..main import app
from .test_operations import create_user, login_user, delete_user

client = TestClient(app)

def test_user_login():
    create_user()
    
    response = client.post("/user-login", json={'username': 'pytestuser1', 'pincode': '0000'})

    delete_user()

    assert response.status_code == 200
    assert response.json() == {"Message" : "User logged in successfully."}

def test_user_login_nonexistent_username():
    response = client.post('/user-login', json={'username': 'pytestuser', 'pincode': '1010'})

    assert response.status_code == 404
    assert response.json() == {'detail': 'Username does not exist.'}

def test_user_login_wrong_credentials():
    create_user()

    response = client.post("/user-login", json={'username': 'pytestuser1', 'pincode': '1111'})

    #logging in for deletion
    login_user()
    delete_user()

    assert response.status_code == 401
    assert response.json() == {'detail': "User credentials don't match"}

def test_user_logout():
    create_user()
    login_user()

    response = client.post('/user-logout')

    login_user()
    delete_user()

    assert response.status_code == 200
    assert response.json() == {"Message" : "User logged out successfully."}

def test_user_logout_without_login():
    create_user()

    response = client.post('/user-logout')

    #login to delete
    login_user()
    delete_user()

    assert response.status_code == 403
    assert response.json() == {'detail': 'User not logged in'}


