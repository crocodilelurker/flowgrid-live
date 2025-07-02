from bson import ObjectId
from configurations import ItemCollection
async def get_prev_transaction(id:str):
    item_id=ObjectId(id)
    prev_transaction=[]
    item= await ItemCollection.find_one({"_id": ObjectId(item_id)})
    prev_transaction=item.get("prev_transaction",[])
    return prev_transaction