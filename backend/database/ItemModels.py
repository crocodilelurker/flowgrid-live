from pydantic import BaseModel
from datetime import datetime
class Item_Uplink(BaseModel):
    name:str
    title:str
    value:int=0
    issuer_id:str
    created_at:int = int(datetime.timestamp(datetime.now()))


