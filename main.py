from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from account_ops import Account, accountCredentials, accounts, updateAccountDatabase
from auth import router as auth_router
from operations import router as operations_router

app = FastAPI()

@app.get("/")
async def main():
    """ this is the entry point of the application. """
    return {"Message" : "Application successfully loaded."}


app.include_router(auth_router)
app.include_router(operations_router)
