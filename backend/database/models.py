from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username:str
    email:str
    balance:float=0.0
    password:str
    items:list[str]=[]
    created_at:int = int(datetime.timestamp(datetime.now()))
    fernet_key:str = None


class Transaction(BaseModel):
    amount:float
    sender_id:str
    receiver_id:str
    created_at:int =int(datetime.timestamp(datetime.now()))

class User_Auth(BaseModel):
    username:str
    password:str