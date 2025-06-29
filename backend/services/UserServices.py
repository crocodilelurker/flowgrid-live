from fastapi import Request, HTTPException
from configurations import UserCollection
from utils.verify_jwt import verify_jwt
from bson import ObjectId

async def get_balance(request:Request):
    #we get the user_id from the jwt token
    #and then we get the user from the database
    try:
        token_payload=verify_jwt(request)
        user_id = token_payload.get("user_id")
        user = await UserCollection.find_one({"_id": ObjectId(user_id)})
        return user['balance']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user balance: {str(e)}")
    
async def get_user_id(request: Request):
    token_payload = verify_jwt(request)
    return token_payload.get("user_id")