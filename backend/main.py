from fastapi import FastAPI
from auth import router as auth_router
from operations import router as operations_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"]
)

@app.get("/")
async def main():
    """ this is the entry point of the application. """
    return {"Message" : "Application successfully loaded."}


app.include_router(auth_router)
app.include_router(operations_router)
