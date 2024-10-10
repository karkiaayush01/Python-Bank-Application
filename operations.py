#this module handles all the operations of the account

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from account_ops import accounts, Account
from database import addToDatabase, get_insertion_id, editDatabaseInformation, deleteFromDatabase
from auth import admin_auth, user_auth

class moneyRequest(BaseModel): #this basemodel uses money as instance variable and is used for withdrawal and deposit
    amount: float

router = APIRouter()

@router.post("/create")
async def create(account: Account, auth: None = Depends(admin_auth)): #Passing an instance of Account as response body
    if account.username in accounts:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    
    if len(account.pincode) != 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Pincode should be 4 digits long.")
    
    accounts[account.username] = account
    addToDatabase(account)
    
    return {"Message" : "Account created Successfully."}

@router.post("/get-balance") #using post even to get balance because get will not allow response bodies and passing details as parameters exposes the pincode in url
async def get_balance(admin_auth: None = Depends(admin_auth), user_auth: None = Depends(user_auth)):
    from auth import current_user
    return {"Balance": current_user.balance}

@router.post("/withdraw")
async def withDraw_balance(withdrawAmt: moneyRequest, admin_auth: None = Depends(admin_auth), user_auth: None = Depends(user_auth)): 
    from auth import current_user
    if withdrawAmt.amount > current_user.balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Specified amount exceeds account balance.")
    else:
        current_user.balance -= withdrawAmt.amount
        insertion_id = get_insertion_id(current_user)
        editDatabaseInformation(current_user, insertion_id)
    
    return {"Message": "Balance withdrawn successfully."}

@router.post("/deposit")
async def deposit_balance(depositAmt: moneyRequest, admin_auth: None = Depends(admin_auth), user_auth: None = Depends(user_auth)):
    from auth import current_user
    current_user.balance += depositAmt.amount
    insertion_id = get_insertion_id(current_user)
    editDatabaseInformation(current_user, insertion_id)
    
    return {"Message": "Balance deposited successfully."}

@router.delete("/delete")
async def delete_user(auth: None = Depends(admin_auth), user_auth: None = Depends(user_auth)):
    from auth import current_user, clear_user_session
    if(current_user.balance > 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account still holds balance. Withdraw balance completely before deletion.")
    
    del(accounts[current_user.username])
    insertion_id = get_insertion_id(current_user)
    deleteFromDatabase(insertion_id)
    clear_user_session()
    
    return {"Message": "Account deleted successfully"}