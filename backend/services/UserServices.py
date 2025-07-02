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
async def admin_convert(token_payload):
    try:
        user_id= token_payload.get("user_id")
        #updating user with admin status to True
        await UserCollection.find_one_and_update({"_id":ObjectId(user_id)},{"$set": {"is_admin": True}})
        return True;
    except Exception as e:
        print(f"Invalid response from the API: {str(e)}")
        return False
async def admin_stat(request:Request):
    token_payload=verify_jwt(request)
    try:
        user_id= token_payload.get("user_id")
        user = await UserCollection.find_one({"_id": ObjectId(user_id)})
        is_admin=user.get("is_admin",False)
        if(is_admin==True):
            print("Is a Admin")
            return True
        else:
            print("Not a Admin")
            return False
    except Exception as e:
        return {"message":"Error Retrieving is_admin"}

async def get_items_list(user:str):
    user_id=ObjectId(user)
    try:
        User=await UserCollection.find_one({"_id":user_id})
    except Exception as e:
        return {"message":"Error in finding User","error":str(e)}
    items_list=[]
    try:
        items_list=User.get("items",[])
    except Exception as e:
        return {"message":"Error in finding User List","error":str(e)}
    return items_list