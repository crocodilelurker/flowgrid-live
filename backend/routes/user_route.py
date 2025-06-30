from fastapi import APIRouter,Request,Response
from database.models import User,Create_User
from configurations import UserCollection
from bson import ObjectId
from utils.passkey import hash_password
from utils.verify_jwt import verify_jwt
from services.UserServices import generate_key,admin_convert
router = APIRouter(prefix="/users", tags=["Users"])
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live! User API"}

@router.post("/create-user")
async def create_user(user:Create_User,request:Request,response:Response):
    if not verify_jwt(request):
        try:
            hashed_password = hash_password(user.password)
            user.password = hashed_password
            fern=generate_key()
            user_data=User(
                username=user.username,
                email=user.email,
                password=user.password,
                fernet_key=fern
            )
            existing_user = await UserCollection.find_one({"username": user.username})
            if existing_user:
                return {"status_code": 400, "message": "User already exists"}
            result= await UserCollection.insert_one(dict(user_data))
            return {"status_code": 201, "message": "User created successfully", "user_id": str(result.inserted_id),"fernet_key":str(fern)}
        except Exception as e:
            return {"status_code": 500, "message": "Error creating user", "error": str(e)}
    else:
        return{"status_code":400,"message":"Already Logged In"}
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
async def get_user(user_id: str, request: Request):
    try:
        #if the user has a jwt token in cookies only then he can access this endpoint
        if not verify_jwt(request):
            return {"status_code": 401, "message": "Unauthorized access"}
        user = await UserCollection.find_one({"_id": ObjectId(user_id)})
        if user:
            return {"status_code": 200, "message": "User found", "user": convert_object_id_to_str(user)}
        else:
            return {"status_code": 404, "message": "User not found"}
    except Exception as e:
        return {"status_code": 500, "message": "Error retrieving user", "error": str(e)}

@router.get("/admin-converter")
async def admin_converter(request:Request):
    #verify JWT token 
    try:
        token_payload=verify_jwt(request)
        if not token_payload:
            return {"status_code": 401, "message": "Unauthorized access"}
        result = await admin_convert(token_payload)
        if(result):
            return {"message":"Authorized Admin"}
        else:
            return {"status_code":500, "message":"Error Resolving Admin"}
        
    except Exception as e:
        return {"status_code": 500, "message": "Error retrieving admin_status", "error": str(e)}
