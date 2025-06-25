from fastapi import APIRouter
from fastapi import FastAPI
from configurations import connectDB
from contextlib import asynccontextmanager
from database.models import User, Transaction
from configurations import UserCollection, TransactionCollection
@asynccontextmanager
async def lifespan(app: FastAPI):
    connectDB()
    yield
    print("Shutting down the application...")
app = FastAPI(lifespan=lifespan)
router = APIRouter()
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live!"}

@router.post("/create-user")
async def create_user(user:User):
    try:
        result= await UserCollection.insert_one(dict(user))
        return {"status_code": 201, "message": "User created successfully", "user_id": str(result.inserted_id)}
    except Exception as e:
        return {"status_code": 500, "message": "Error creating user", "error": str(e)}

app.include_router(router)
