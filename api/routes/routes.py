from fastapi import APIRouter
from fastapi import HTTPException
from cryptography.fernet import Fernet
from pydantic import BaseModel

router = APIRouter()
class EncrpytRequest(BaseModel):
    key: str
    data: str

@router.get("/")
def root():
    return {"message": "Welcome to the Flowgrid fernet api"}
@router.get("/generate_key")
async def key_generator():
    try:
        key= Fernet.generate_key()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    #return with status code 200
    return {
        "key":key
    }
    
@router.post("/encrypt")
async def encrypt(request: EncrpytRequest):
    try:
        fernet = Fernet(request.key.encode())
        encrypted_data = fernet.encrypt_at_time(request.data.encode())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "encrypted_data": encrypted_data
    }
@router.post("/decrypt")
async def decrypt(request: EncrpytRequest):
    try:
        fernet = Fernet(request.key.encode())
        decrypted_data = fernet.decrypt(request.data.encode()).decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "decrypted_data": decrypted_data
    }
