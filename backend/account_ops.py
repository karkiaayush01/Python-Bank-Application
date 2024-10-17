#this module contains functions regarding account operations such as creating account, validating user input, and performing actions on accounts

from pydantic import BaseModel
from database import getAccounts

class Account(BaseModel): #creating a basemodel object for auto validation
    username: str
    pincode: str
    balance: float

class accountCredentials(BaseModel): #this basemodel is required by operations that only require username and pincode.
    username: str
    pincode: str

class Transaction(BaseModel):
    username: str
    amount: float
    type: str
    dateTime: str

accounts = getAccounts() #initial account dictionary.