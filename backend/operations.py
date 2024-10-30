#this module handles all the operations of the account

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import datetime

from .account_ops import Account, Transaction
from .database import getUserData, get_insertion_id, editDatabaseInformation, deleteFromDatabase, addTransactionInfoToDB, getRecentTransactions
from .auth import oauth2_scheme, cognito_client

class moneyRequest(BaseModel): #this basemodel uses money as instance variable and is used for withdrawal and deposit
    amount: float

router = APIRouter()

@router.get("/get-username")
async def get_username(access_token: str = Depends(oauth2_scheme)):
    try:
        response = cognito_client.get_user(AccessToken = access_token)
        username = response['Username']
        return {'username': username}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/get-user-data") #using post even to get balance because get will not allow response bodies and passing details as parameters exposes the password in url
async def get_user_data(access_token: str = Depends(oauth2_scheme)):
    try:
        response = cognito_client.get_user(AccessToken = access_token)
        username = response['Username']
        userData = getUserData(username)
        return {
            'username': userData.username,
            'balance': userData.balance
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/get-balance") #using post even to get balance because get will not allow response bodies and passing details as parameters exposes the password in url
async def get_user_data(access_token: str = Depends(oauth2_scheme)):
    try:
        response = cognito_client.get_user(AccessToken = access_token)
        username = response['Username']
        userData = getUserData(username)
        return {
            'balance': userData.balance
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/get-recent-transactions")
async def get_recent_transactions(access_token: str = Depends(oauth2_scheme)):
    response = cognito_client.get_user(AccessToken = access_token)
    username = response['Username']
    transactions = getRecentTransactions(username)
    return {'Transactions' : transactions}

@router.post("/withdraw")
async def withdraw_balance(withdrawAmt: moneyRequest, access_token: str = Depends(oauth2_scheme)): 
    response = cognito_client.get_user(AccessToken = access_token)
    username = response['Username']
    userData = getUserData(username)
    if withdrawAmt.amount > userData.balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Specified amount exceeds account balance.")
    else:
        userData.balance -= withdrawAmt.amount
        insertion_id = get_insertion_id(userData.username)
        editDatabaseInformation(userData, insertion_id)

        current_date_time = datetime.datetime.now().isoformat()
        transaction_data = Transaction(username=userData.username, amount=withdrawAmt.amount, type='withdraw', dateTime=current_date_time)
        addTransactionInfoToDB(transaction_data)
    
    return {"message": "Balance withdrawn successfully."}

@router.post("/deposit")
async def deposit_balance(depositAmt: moneyRequest, access_token: str = Depends(oauth2_scheme)):
    response = cognito_client.get_user(AccessToken = access_token)
    username = response['Username']
    userData = getUserData(username)
    userData.balance += depositAmt.amount
    insertion_id = get_insertion_id(userData.username)
    editDatabaseInformation(userData, insertion_id)
    current_date_time = datetime.datetime.now().isoformat()
    transaction_data = Transaction(username=userData.username, amount=depositAmt.amount, type='deposit', dateTime=current_date_time)
    addTransactionInfoToDB(transaction_data)
    
    return {"message": "Balance deposited successfully."}

@router.delete("/delete")
async def delete_user():
    from .auth import current_user, clear_user_session
    if(current_user.balance > 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account still holds balance. Withdraw balance completely before deletion.")
    
    insertion_id = get_insertion_id(current_user)
    deleteFromDatabase(insertion_id)
    clear_user_session()
    
    return {"Message": "Account deleted successfully"}
