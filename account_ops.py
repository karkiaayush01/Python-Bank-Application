#this module contains functions regarding account operations such as creating account, validating user input, and performing actions on accounts

from pydantic import BaseModel

import csv

class Account(BaseModel): #creating a basemodel object for auto validation
    username: str
    pincode: str
    balance: float

class accountCredentials(BaseModel): #this basemodel is required by operations that only require username and pincode.
    username: str
    pincode: str

class alteringAccount(BaseModel): #this basemodel is for updating balance (withdraw/deposit). It uses an amount instance variable
    username: str
    pincode: str
    amount: float

def addToDatabase(account):
    is_first_record = False

    if len(accounts) == 1: #checking if this is the 1st account in the database
        is_first_record = True

    newAccount = [account.username, account.pincode, str(account.current_balance)]
    with open('accounts.csv', mode='a', newline='') as file: #using newline as '' because csv writer leaves a newline by default. It prevents a blank line
        account_writer = csv.writer(file)

        if is_first_record:
            file.write('')
            is_first_record: False

        #Appending new records
        account_writer.writerow(newAccount)

def updateAccountDatabase(accounts):
    header = ['username', 'pincode', 'balance']
    with open('accounts.csv', mode = 'w', newline='') as file:
        accounts_writer = csv.writer(file)
        accounts_writer.writerow(header)
        for account in accounts.values():
            row = [account.username, account.pincode, account.balance]
            accounts_writer.writerow(row)


def getAccounts():
    accounts = {} #empty dictionary

    with open('accounts.csv', mode='r') as file:
        accounts_reader = csv.reader(file)
        next(accounts_reader) #skipping the 1st (header) row
        for row in accounts_reader:
            username = row[0]
            pincode = row[1]
            balance = row[2]
            accounts[username] = Account(username = username, pincode=pincode, balance=float(balance))
            
    return accounts

accounts = getAccounts() #initial account dictionary.