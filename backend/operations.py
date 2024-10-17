#this module handles all the operations of the account

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import datetime

from account_ops import accounts, Account, Transaction
from database import addUserToDatabase, get_insertion_id, editDatabaseInformation, deleteFromDatabase, addTransactionInfoToDB, getRecentTransactions
from auth import user_auth

class moneyRequest(BaseModel): #this basemodel uses money as instance variable and is used for withdrawal and deposit
    amount: float

router = APIRouter()

@router.post("/create")
async def create(account: Account): #Passing an instance of Account as response body
    if account.username == '' or account.pincode == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = 'Empty fields found.')
    if account.username in accounts:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    
    if len(account.pincode) != 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Pincode should be 4 digits long.")
    
    if(account.balance <= 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount should be greater than 0.")
          
    accounts[account.username] = account
    addUserToDatabase(account)

    current_date_time = datetime.datetime.now().isoformat()
    transaction_data = Transaction(username=account.username, amount = account.balance, type='deposit', dateTime=current_date_time)
    addTransactionInfoToDB(transaction_data)
    
    return {"message" : "Account created successfully."}

@router.get("/get-user-data")
async def get_user_data(user_auth: None = Depends(user_auth)):
    from auth import current_user
    return{"username": current_user.username,
           "balance": current_user.balance
           }

@router.get("/get-balance") #using post even to get balance because get will not allow response bodies and passing details as parameters exposes the pincode in url
async def get_balance(user_auth: None = Depends(user_auth)):
    from auth import current_user
    return {"Balance": current_user.balance}

@router.get("/get-recent-transactions")
async def get_recent_transactions(user_auth: None = Depends(user_auth)):
    from auth import current_user
    transactions = getRecentTransactions(current_user.username)
    return {'Transactions' : transactions}

@router.get("/get-logged-in-status") #this endpoint gives information of whether user is still logged in so that the frontend doesn't sign out on each reload
async def get_logged_in_status():
    from auth import current_user
    if current_user != None:
        return {"message": "true"}
    
    return{"message": "false"}

@router.post("/withdraw")
async def withDraw_balance(withdrawAmt: moneyRequest, user_auth: None = Depends(user_auth)): 
    from auth import current_user
    if withdrawAmt.amount > current_user.balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Specified amount exceeds account balance.")
    else:
        current_user.balance -= withdrawAmt.amount
        insertion_id = get_insertion_id(current_user)
        editDatabaseInformation(current_user, insertion_id)

        current_date_time = datetime.datetime.now().isoformat()
        transaction_data = Transaction(username=current_user.username, amount=withdrawAmt.amount, type='withdraw', dateTime=current_date_time)
        addTransactionInfoToDB(transaction_data)
    
    return {"message": "Balance withdrawn successfully."}

@router.post("/deposit")
async def deposit_balance(depositAmt: moneyRequest, user_auth: None = Depends(user_auth)):
    from auth import current_user
    current_user.balance += depositAmt.amount
    insertion_id = get_insertion_id(current_user)
    editDatabaseInformation(current_user, insertion_id)
    current_date_time = datetime.datetime.now().isoformat()
    transaction_data = Transaction(username=current_user.username, amount=depositAmt.amount, type='deposit', dateTime=current_date_time)
    addTransactionInfoToDB(transaction_data)
    
    return {"message": "Balance deposited successfully."}

@router.delete("/delete")
async def delete_user(user_auth: None = Depends(user_auth)):
    from auth import current_user, clear_user_session
    if(current_user.balance > 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account still holds balance. Withdraw balance completely before deletion.")
    
    del(accounts[current_user.username])
    insertion_id = get_insertion_id(current_user)
    deleteFromDatabase(insertion_id)
    clear_user_session()
    
    return {"Message": "Account deleted successfully"}
