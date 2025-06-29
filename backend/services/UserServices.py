from fastapi import Request, HTTPException
from configurations import UserCollection
from utils.verify_jwt import verify_jwt
from bson import ObjectId
import requests

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

def generate_key():
    try:
        url = "http://127.0.0.1:5000/generate_key/"
        response = requests.get(url)
        if response.status_code == 200:
            data=response.json()
            if "key" in data:
                return data["key"]  # Return the generated key
            else:
                raise ValueError("The response does not contain a 'key' field.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling the API: {str(e)}")
        return None
    
    except ValueError as ve:
        print(f"Invalid response from the API: {str(ve)}")
        return None
