from fastapi import APIRouter,Response,Request
from configurations import UserCollection
from database.models import User_Auth
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils.passkey import verify_password
import os,jwt
load_dotenv()
JWT_EXPIRY_TIME = int(os.getenv("JWT_EXPIRY_TIME", 3600))
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live! Authentication API"}

@router.post("/login")
async def login(user: User_Auth,response: Response):
    try:
        user_data = await UserCollection.find_one({"username": user.username})
        if user_data and verify_password(user.password, user_data["password"]):
            token_payload = {"user_id": str(user_data["_id"]), "username": user_data["username"],"exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRY_TIME) }
            jwt_token = jwt.encode(token_payload, SECRET_KEY, algorithm=os.getenv("JWT_ALGORITHM", "HS256"))
            response.set_cookie(key="jwt_token", value=jwt_token, httponly=True, samesite="lax")
            return {"status_code": 200, "message": "Login successful", "user_id": str(user_data["_id"])}
        else:
            return {"status_code": 401, "message": "Invalid credentials"}
    except Exception as e:
        return {"status_code": 500, "message": "Error during login", "error": str(e)}
    
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="jwt_token")
    return {"status_code": 200, "message": "Logout successful"}
@router.get("/verify-token")
async def verify_token(request: Request, response: Response):
    jwt_token = request.cookies.get("jwt_token")
    if not jwt_token:
        return {"status_code": 401, "message": "No token provided"}
    
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[os.getenv("JWT_ALGORITHM", "HS256")])
        return {"status_code": 200, "message": "Token is valid", "user_id": payload["user_id"], "username": payload["username"]}
    except jwt.ExpiredSignatureError:
        return {"status_code": 401, "message": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"status_code": 401, "message": "Invalid token"}
