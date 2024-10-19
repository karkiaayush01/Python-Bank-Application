from fastapi.testclient import TestClient
from ..main import app
from ..database import deleteFromDatabase, get_insertion_id

client = TestClient(app)

def create_user(username = 'pytestuser1', pincode = '0000', balance = 1000):
    response = client.post("/create", json={'username': username, 'pincode': pincode, 'balance': balance})
    assert response.json() == {"message" : "Account created successfully."}

def login_user(username = 'pytestuser1', pincode = '0000'):
    client.post("/user-login", json={'username': username, 'pincode': '0000'})

def delete_user():
    client.post("/withdraw", json={'amount': 1000}) #withdrawing whole balance before deletion to avoid error
    client.delete("/delete")

def test_create():
    response = client.post("/create", json={'username': 'pytestuser1', 'pincode': '0000', 'balance': 1000})

    login_user()
    delete_user()

    assert response.status_code == 200
    assert response.json() == {"message" : "Account created successfully."}

def test_create_invalid_input():
    #null username and pincode
    response = client.post('/create', json={'username': '', 'pincode': '', 'balance': 1000})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Empty fields found.'}

    #pincode not 4 digits long
    response = client.post('/create', json={'username':'pytestuser1', 'pincode':'000', 'balance':1000})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Pincode should be 4 digits long.'}

    #amount less than or equal to 0
    response = client.post('/create', json={'username':'pytestuser1', 'pincode':'0000', 'balance':-100})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Amount should be greater than 0.'}

    #creating similar user twice
    client.post('/create', json={'username': 'pytestuser1', 'pincode': '0000', 'balance': 1000})
    response = client.post('/create', json={'username':'pytestuser1', 'pincode':'2000', 'balance':1000})
    assert response.status_code == 409
    assert response.json() == {'detail': 'User already exists.'}
    login_user()
    delete_user()

    #posting string balance
    response = client.post('/create', json={'username': 'pytestuser1', 'pincode': '0000', 'balance': '1000a'})
    expected_response = {
        'detail': [
            {
                'input': '1000a',
                'loc': ['body', 'balance'],
                'msg': 'Input should be a valid number, unable to parse string as a number',
                'type': 'float_parsing'
            }
        ]
    }
    assert response.status_code == 422
    assert response.json() == expected_response

    #posting integer pincode
    response = client.post('/create', json={'username': 'pytestuser1', 'pincode':1000, 'balance': 1000})
    expected_response = {
        "detail": [
            {
            "type": "string_type",
            "loc": [
                "body",
                "pincode"
            ],
            "msg": "Input should be a valid string",
            "input": 1000
            }
        ]
    }

    assert response.status_code == 422
    assert response.json() == expected_response


def test_get_user_data():
    create_user()
    login_user()

    response = client.get("/get-user-data")

    delete_user()

    assert response.status_code == 200
    assert response.json() == {'username': 'pytestuser1', 'balance': 1000}

def test_get_user_data_without_login():
    create_user()

    response = client.get('/get-user-data')

    #logging in for deletion
    login_user()
    delete_user()

    assert response.status_code == 403
    assert response.json() == {'detail': 'User not logged in'}

def test_get_balance():
    create_user()
    login_user()

    response = client.get("/get-balance")

    delete_user()

    assert response.status_code == 200
    assert response.json() == {'Balance': 1000}

def test_get_balance_without_login():
    create_user()

    response = client.get('/get-balance')

    #logging in for deletion
    login_user()
    delete_user()
    
    assert response.status_code == 403
    assert response.json() == {'detail': 'User not logged in'}

def test_get_recent_transactions():
    create_user()
    login_user()

    response = client.get("/get-recent-transactions")

    delete_user()

    assert response.status_code == 200
    datetime = response.json()['Transactions'][0]['dateTime']
    assert response.json() == {'Transactions': [{'username': 'pytestuser1', 'amount':1000, 'type': 'deposit', 'dateTime': datetime}]}

def test_get_recent_transactions_without_login():
    create_user()

    response = client.get("/get-recent-transactions")

    #logging in for deletion
    login_user()
    delete_user()

    assert response.status_code == 403
    assert response.json() == {'detail': 'User not logged in'}

def test_get_logged_in_status():
    create_user()
    login_user()

    response = client.get("/get-logged-in-status")

    delete_user()

    assert response.status_code == 200
    assert response.json() == {'message': 'true'}

def test_get_logged_in_status_without_login():
    create_user()

    response = client.get("/get-logged-in-status")

    #logging in for deletion
    login_user()
    delete_user()

    assert response.status_code == 200
    assert response.json() == {'message': 'false'}

def test_withdraw_balance():
    create_user(balance=1100)
    login_user()

    response = client.post("/withdraw", json={'amount': 100})

    delete_user()

    assert response.status_code == 200
    assert response.json() == {'message': 'Balance withdrawn successfully.'}

def test_withdraw_balance_without_login():
    create_user()

    response = client.post('/withdraw', json={'amount': 1000})

    #logging in for deletion
    login_user()
    delete_user()

    assert response.status_code == 403
    assert response.json() == {'detail': 'User not logged in'}

def test_withdraw_balance_exceeding_current_balance():
    create_user()
    login_user()

    response = client.post("/withdraw", json={'amount': 1100})

    delete_user()

    assert response.status_code == 400
    assert response.json() == {'detail': 'Specified amount exceeds account balance.'}

def test_deposit_balance():
    client.post("/create", json={'username': 'pytestuser1', 'pincode': '0000', 'balance': 900})
    client.post("/user-login", json={'username': 'pytestuser1', 'pincode': '0000'})

    response = client.post("/deposit", json={'amount': 100})

    delete_user()

    assert response.status_code == 200
    assert response.json() == {'message': 'Balance deposited successfully.'}

def test_deposit_balance_without_login():
    create_user()

    response = client.post('/deposit', json={'amount': 1000})

    #logging in for deletion
    login_user()
    delete_user()

    assert response.status_code == 403
    assert response.json() == {'detail': 'User not logged in'}

def test_delete():
    create_user()
    login_user()

    client.post("/withdraw", json={'amount': 1000})

    response = client.delete("/delete")

    assert response.status_code == 200
    assert response.json() == {'Message': 'Account deleted successfully'}

def test_delete_without_login():
    create_user()
    
    response = client.delete("/delete")

    #login for deletion
    login_user()
    delete_user()

    assert response.status_code == 403
    assert response.json() == {'detail': 'User not logged in'}


