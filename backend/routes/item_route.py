from fastapi import APIRouter,Request
from services.UserServices import admin_stat
from database.ItemModels import Item_Uplink,Item_Log
from configurations import ItemCollection
from datetime import datetime
from services.UserServices import get_user_id
from bson import ObjectId
from utils.verify_jwt import verify_jwt
router= APIRouter(prefix="/item",tags=["Items"])
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live! Items API"}

@router.post("/add-items")
async def add_items(request:Request, item:Item_Log):
    #we need to verufy that he is admin or not
    #we use services
    is_admin= await admin_stat(request)
    print(is_admin)
    if(is_admin):      
        try:
            item_data=Item_Uplink(
                name=item.name,
                title=item.title,
                value=item.value,
                issuer_id=await get_user_id(request),
                created_at= int(datetime.timestamp(datetime.now())),
                prev_transaction=item.prev_transaction,
                current_owner=""
            )
            result = await ItemCollection.insert_one(dict(item_data)) 
            return {"status_code": 201, "message": "Item created successfully", "item_id": str(result.inserted_id)}
        except Exception as e:
            return {"status_code": 500, "message": "Error during adding", "error": str(e)}
    else:
        #code for issuing the new item to the user 
        try:
            item_data=Item_Uplink(
                name=item.name,
                title=item.title,
                value=item.value,
                issuer_id=await get_user_id(request),
                created_at= int(datetime.timestamp(datetime.now())),
                prev_transaction=[str(await get_user_id(request))],
                current_owner=await get_user_id(request)
            )
            result = await ItemCollection.insert_one(dict(item_data)) 
            return {"status_code": 201, "message": "Item created successfully", "item_id": str(result.inserted_id)}
        except Exception as e:
            return {"status_code": 500, "message": "Error during adding", "error": str(e)}
    
def convert_object_id_to_str(data):
    if isinstance(data, dict): 
        return {k: convert_object_id_to_str(v) for k, v in data.items()}
    elif isinstance(data, list): 
        return [convert_object_id_to_str(item) for item in data]
    elif isinstance(data, ObjectId): 
        return str(data)
    else:
        return data

@router.get("/fetch-item/{item_id}")
async def fetch_item(item_id: str, request: Request):
    try:
        #if the user has a jwt token in cookies only then he can access this endpoint
        if not verify_jwt(request):
            return {"status_code": 401, "message": "Unauthorized access"}
        item = await ItemCollection.find_one({"_id": ObjectId(item_id)})
        if item:
            return {"status_code": 200, "message": "Item found", "item": convert_object_id_to_str(item)}
        else:
            return {"status_code": 404, "message": "Item not found"}
    except Exception as e:
        return {"status_code": 500, "message": "Error retrieving Item", "error": str(e)}
