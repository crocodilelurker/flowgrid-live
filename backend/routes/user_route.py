from fastapi import APIRouter
from database.models import User
from configurations import UserCollection
from bson import ObjectId
router = APIRouter(prefix="/users", tags=["Users"])
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live! User API"}

@router.post("/create-user")
async def create_user(user:User):
    try:
        result= await UserCollection.insert_one(dict(user))
        return {"status_code": 201, "message": "User created successfully", "user_id": str(result.inserted_id)}
    except Exception as e:
        return {"status_code": 500, "message": "Error creating user", "error": str(e)}
def convert_object_id_to_str(data):
    if isinstance(data, dict): 
        return {k: convert_object_id_to_str(v) for k, v in data.items()}
    elif isinstance(data, list): 
        return [convert_object_id_to_str(item) for item in data]
    elif isinstance(data, ObjectId): 
        return str(data)
    else:
        return data

@router.get("/get-user/{user_id}")
async def get_user(user_id: str):
    try:
        user = await UserCollection.find_one({"_id": ObjectId(user_id)})
        if user:
            return {"status_code": 200, "message": "User found", "user": convert_object_id_to_str(user)}
        else:
            return {"status_code": 404, "message": "User not found"}
    except Exception as e:
        return {"status_code": 500, "message": "Error retrieving user", "error": str(e)}
