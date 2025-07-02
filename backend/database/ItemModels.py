from pydantic import BaseModel
from datetime import datetime
class Item_Uplink(BaseModel):
    name:str
    title:str
    value:int=0
    issuer_id:str
    created_at:int = int(datetime.timestamp(datetime.now()))
    prev_transaction:list[str]=[]
    current_owner:str=""

class Item_Log(BaseModel):
    name:str
    title:str
    value:int
    prev_transaction:list[str]=[]

class Item_Transacton:
    name:str
    receiver_id:str
    sender_id:str