#this module handles the admin and user authorization

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .account_ops import Account, AuthDetails, ConfirmationModel

import boto3
import datetime
from .account_ops import Transaction
from .database import addTransactionInfoToDB, addUserToDatabase, getUserData
import requests
from jose import JWTError, jwt

router = APIRouter()

#AWS Cognito Config
CLIENT_ID = '6gt5gpdm0e5j2oucr9ri7n8aqf'
REGION = 'eu-north-1'
USER_POOL_ID = "eu-north-1_luIIH3MxZ"
COGNITO_JWK_URL = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"

#Retrieving jwks key from cognito
jwks = requests.get(COGNITO_JWK_URL).json()

cognito_client = boto3.client('cognito-idp', region_name=REGION)

#OAuth2Scheme for JWT Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

current_user = None #changes after user login

@router.post("/sign-up")
def signup(user: Account):
    try:
        response = cognito_client.sign_up(
            ClientId = CLIENT_ID,
            Username = user.username,
            Password = user.password,
            UserAttributes = [
                {'Name': 'email', 'Value': user.email}
            ]
        )
        if response:
            addUserToDatabase(user)
            current_date_time = datetime.datetime.now().isoformat()
            transaction_data = Transaction(username=user.username, amount = user.balance, type='deposit', dateTime=current_date_time)
            addTransactionInfoToDB(transaction_data)
            return {'message': 'Account created successfully.'}
        
    except cognito_client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")
    except Exception as e:
        if hasattr(e, 'response') and ('Error' in e.response):
            detailMessage = e.response['Error']['Message']
        else:
            detailMessage = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= detailMessage)
    
@router.post("/confirmation")
def confirmation(userData: ConfirmationModel):
    try:
        response = cognito_client.confirm_sign_up(
            ClientId = CLIENT_ID,
            Username = userData.username,
            ConfirmationCode = userData.confirmationCode
        )

        return{'message': 'Confirmed Successfully'}
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except cognito_client.exceptions.CodeMismatchException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid confirmation code")
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this action")
    except cognito_client.exceptions.ExpiredCodeException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmation code has expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during confirmation")

@router.post("/sign-in")
def signin(user: AuthDetails):
    try:
        response = cognito_client.initiate_auth(
            AuthFlow = 'USER_PASSWORD_AUTH',
            AuthParameters= {
                'USERNAME': user.username,
                'PASSWORD': user.password
            },
            ClientId = CLIENT_ID
        )
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']
        global current_user
        current_user = getUserData(user.username)
        return{
            'AccessToken': access_token,
            'RefreshToken': refresh_token
        }
        
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except Exception as e:
        if hasattr(e, 'response') and ('Error' in e.response):
            detailMessage = e.response['Error']['Message']
        else: 
            detailMessage = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detailMessage)
    
@router.post("/sign-out")
def sign_out(access_token: str = Depends(oauth2_scheme)):
    try:
        response = cognito_client.global_sign_out(
            AccessToken = access_token
        )
        clear_user_session()
        return {"message": "Successfully logged out."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/validate-token")
def validate_token(access_token: str = Depends(oauth2_scheme)):
    try:
        # Decode and validate the token using JWKS
        payload = jwt.decode(access_token, jwks, algorithms=["RS256"], audience=CLIENT_ID)
        return {"status": "valid"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
def clear_user_session():
    global current_user
    current_user = None