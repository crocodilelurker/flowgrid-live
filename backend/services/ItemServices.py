from bson import ObjectId
from configurations import ItemCollection,UserCollection
from fastapi import Request
from services.UserServices import get_balance,get_user_id,get_items_list
async def get_prev_transaction(id:str):
    item_id=ObjectId(id)
    prev_transaction=[]
    item= await ItemCollection.find_one({"_id": ObjectId(item_id)})
    prev_transaction=item.get("prev_transaction",[])
    return prev_transaction

async def return_currowner(id:str):
    try:
        item= await ItemCollection.find_one({"_id": ObjectId(id)})
        curr_owner=item.get("current_owner",False)
        return curr_owner
    except Exception as e:
        return {"message":"Unavailable Item Service","error":str(e)}
    
async def validate_item_transaction(item:str,sender:str,request:Request):
    sender_id=ObjectId(sender)
    try:
        user_id = get_user_id(request)
        items_list=get_items_list(user_id)
        #now we need to check whether the items_list contains the item or not
        if str(item) in [str(i) for i in items_list]:
            return True
        else:
            return False
    except Exception as e:
        return {"message":"Unavailable Item Service","error":str(e)}

async def update_item_transaction(receiver:str,sender:str,item:str):
    receiver_id=ObjectId(receiver)
    sender_id=ObjectId(sender)
    item_id=ObjectId(item)

    updated_item = await UserCollection.find_one_and_update(
        {"_id": item_id},
        {"$push": {"prev_transaction": sender_id}}, 
        return_document=True 
    )
    #now we add and remove item from reciever and sender
    receiver_update_result = await UserCollection.find_one_and_update(
            {"_id": receiver_id},
            {"$push": {"items": item_id}},  
            return_document=True 
        )
    if not receiver_update_result:
            return {"status_code": 404, "message": "Receiver not found"}
    sender_update_result = await UserCollection.find_one_and_update(
            {"_id": sender_id},  
            {"$pull": {"items": item_id}},  
            return_document=True 
        )

    if not sender_update_result:
        return {"status_code": 404, "message": "Sender not found"}
    if updated_item:
        return {
            "status_code": 200,
            "message": "Transaction updated successfully",
            "updated_item": updated_item
        }
    else:
        return {"status_code": 404, "message": "Item not found"}

    