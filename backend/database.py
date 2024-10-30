from pymongo import MongoClient
from bson.objectid import ObjectId


#connecting to db
client = MongoClient('mongodb://localhost:27017/')

db = client.account_db

accounts_coll = db.accounts #getting accounts collection from account_db
transactions_coll = db.transactions #getting transactions collection from account_db

def getUserData(username):
    from .account_ops import userDataModel
    result = accounts_coll.find_one(
        {"username": username}
    )
    return(userDataModel(username=username, balance=result['balance']))

def getRecentTransactions(username):
    from .account_ops import Transaction
    transactions = [] #empty list
    count = 0

    for transaction in transactions_coll.find({'username': username}).sort('date_time', -1):
        transactions.append(Transaction(username = transaction['username'], amount=transaction['amount'], type = transaction['type'], dateTime=transaction['date_time']))
        count+=1
        if count == 5:
            return transactions
        
    return transactions
    

def get_insertion_id(username):
    result = accounts_coll.find_one(
        {'username': username},
        {'_id': 1}
    )
    return result['_id']

def checkEmailInDB(email):
    result = accounts_coll.find_one({'email': email})
    if result:
        return True
    else:
        return False

def addUserToDatabase(account):
    accounts_coll.insert_one({
        "username": account.username,
        "email": account.email,
        "balance": account.balance,
    })

def editDatabaseInformation(userData, insertion_id):
    accounts_coll.update_one(
        {'_id': ObjectId(insertion_id)},
        {'$set' : {
            'username': userData.username,
            'balance': userData.balance
        }}
    )

def deleteFromDatabase(insertion_id):
    username = accounts_coll.find_one({
        '_id': ObjectId(insertion_id)
    })['username']

    accounts_coll.delete_one({'_id': ObjectId(insertion_id)})
    deleteAllUserTransactions(username)
    

def addTransactionInfoToDB(transaction_data):
    transactions_coll.insert_one({
        'username': transaction_data.username,
        'type': transaction_data.type,
        'amount': transaction_data.amount,
        'date_time': transaction_data.dateTime
    })

def deleteAllUserTransactions(username):
    transactions_coll.delete_many({
        'username': username
    })
        

