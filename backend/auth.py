#this module handles the admin and user authorization

from fastapi import APIRouter, Depends, HTTPException, status

from .account_ops import accountCredentials, accounts

router = APIRouter()

current_user = None #changes after user login
    
@router.post("/user-login")
async def user_login(user: accountCredentials):
    global current_user
    if user.username == '' or user.pincode == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty fields found.")
    elif len(user.pincode) != 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pincode should be 4 digits long.")
    username = user.username
    if username in accounts:
        if user.pincode == accounts[username].pincode:
            current_user = accounts[username]
            return {"Message" : "User logged in successfully."}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "User credentials don't match")
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Username does not exist.")


def user_auth():  
    if current_user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not logged in")  
    
@router.post("/user-logout")
async def user_logout(user_auth: None = Depends(user_auth)):
    global current_user
    current_user = None
    return {"Message" : "User logged out successfully."}

def clear_user_session():
    global current_user
    current_user = None