from fastapi import APIRouter
from database.models import User, Transaction
from configurations import UserCollection, TransactionCollection 
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
