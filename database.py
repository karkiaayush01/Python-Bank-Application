from pymongo import MongoClient
from bson.objectid import ObjectId

#connecting to db
client = MongoClient('mongodb://localhost:27017/')

db = client.account_db

accounts_coll = db.accounts #getting accounts collection from account_db

def getAccounts():
    from account_ops import Account
    accounts = {} #empty dictionary

    for account in accounts_coll.find():
        #storing the data in dictionary as Account objects instead of the dictionary returned by the db
        accounts[account['username']] = Account(username = account['username'], pincode = account['pincode'], balance = account['balance'])
            
    return accounts

def get_insertion_id(account):
    result = accounts_coll.find_one(
        {'username': account.username},
        {'_id': 1}
    )
    return result['_id']

def addToDatabase(account):
    accounts_coll.insert_one({
        "username": account.username,
        "pincode" : account.pincode,
        "balance": account.balance
    })

def editDatabaseInformation(account, insertion_id):
    accounts_coll.update_one(
        {'_id': ObjectId(insertion_id)},
        {'$set' : {
            'username': account.username,
            'pincode': account.pincode,
            'balance': account.balance
        }}
    )

def deleteFromDatabase(insertion_id):
    accounts_coll.delete_one({'_id': ObjectId(insertion_id)})
        

