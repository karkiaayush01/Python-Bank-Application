#this module handles the admin and user authorization

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from account_ops import accountCredentials, accounts

router = APIRouter()

class adminPin(BaseModel):
    pincode: str

admin_pin = "1234" #pin required for getting access to admin
current_user = None #changes after user login
admin_logged_in = False

@router.post("/admin-login")
async def admin_login(admin: adminPin):
    global admin_logged_in
    global admin_pin
    if admin.pincode == admin_pin:
        admin_logged_in = True
        return {"Message": "Admin logged in successfully."}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin Pincode does not match.")

def admin_auth():
    if not admin_logged_in:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin authentication required")
    
@router.post("/admin-logout")
async def admin_logout(admin_auth: None = Depends(admin_auth)):
    global admin_logged_in, current_user
    admin_logged_in = False
    current_user = None #logging out of user too if admin logs out
    return {"Message": "Admin logged out successfully."}

    
@router.post("/user-login")
async def user_login(user: accountCredentials, admin_auth: None = Depends(admin_auth)):
    global current_user
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
async def user_logout(admin_auth: None = Depends(admin_auth), user_auth: None = Depends(user_auth)):
    global current_user
    current_user = None
    return {"Message" : "User logged out successfully."}

def clear_user_session():
    global current_user
    current_user = None