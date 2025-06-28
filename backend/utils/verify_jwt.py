#we check if the user has a jwt token in cookies only then he can access this endpoint
from fastapi import Request
import jwt

def verify_jwt(request: Request):
    token = request.cookies.get("jwt_token")
    if not token:
        return False
    else:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        except Exception as e:
            print(f"Error decoding JWT: {str(e)}")
            return False
    
