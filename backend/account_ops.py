#this module contains functions regarding account operations such as creating account, validating user input, and performing actions on accounts

from pydantic import BaseModel

class Account(BaseModel): #creating a basemodel object for auto validation
    username: str
    email: str
    password: str
    balance: float

class ConfirmationModel(BaseModel):
    username: str
    confirmationCode: str

class AuthDetails(BaseModel):
    username: str
    password: str

class userDataModel(BaseModel): #this basemodel is required by operations that only require username and pincode.
    username: str
    balance: float

class Transaction(BaseModel):
    username: str
    amount: float
    type: str
    dateTime: str