from fastapi import APIRouter,Request
from configurations import TransactionCollection
from bson import ObjectId
from utils.verify_jwt import verify_jwt
from database.Service_Models.Transaction_Service import Transaction_Model 
from database.ItemModels import Item_Transacton
from database.models import Item_Transaction
from services.ItemServices import return_currowner,update_item_transaction,validate_item_transaction
from services.TransactionServices import validate_transaction,process_transaction,update_transaction
from services.UserServices import get_user_id
router = APIRouter(prefix="/transactions", tags=["Transactions"])
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live! Transaction API"}
@router.post("/create-transaction")
async def create_transaction(transaction: Transaction_Model, request: Request):
    try:
        if not verify_jwt(request):
            return {"status_code": 401, "message": "Unauthorized access"}
        await validate_transaction(transaction, request)
        await update_transaction(transaction, request)
        await process_transaction(transaction, request)
        return {"status_code": 201, "message": "Transaction created successfully"}
    except Exception as e:
        return {"status_code": 500, "message": "Error creating transaction", "error": str(e)}
def convert_object_id_to_str(data):
    if isinstance(data, dict): 
        return {k: convert_object_id_to_str(v) for k, v in data.items()}
    elif isinstance(data, list): 
        return [convert_object_id_to_str(item) for item in data]
    elif isinstance(data, ObjectId): 
        return str(data)
    else:
        return data
@router.get("/get-transaction/{transaction_id}")
async def get_transaction(transaction_id: str, request: Request):
    try:
        if not verify_jwt(request):
            return {"status_code": 401, "message": "Unauthorized access"}
        transaction = await TransactionCollection.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            return {"status_code": 200, "message": "Transaction found", "transaction": convert_object_id_to_str(transaction)}
        else:
            return {"status_code": 404, "message": "Transaction not found"}
    except Exception as e:
        return {"status_code": 500, "message": "Error retrieving transaction", "error": str(e)}
@router.post("/create-item-transaction/{item_id}")
async def create_item_t(item_id:str,request:Request,item_data:Item_Transacton):
    curr_owner=await return_currowner(item_id)
    if(str(curr_owner)!=str(await get_user_id(request))):
        print(curr_owner)
        print(await get_user_id(request))
        return {"message":"Invalid Credentials"}
    else:
        receiver_id=item_data.receiver_id
        sender_id=str(await get_user_id(request))
        #update_transaction servicein item service 
        try:
            await validate_item_transaction(str(item_id),request)
            await update_item_transaction(receiver_id,sender_id,item_id)
        except Exception as e:
            return{"message":"Error in updating transaction","error":str(e)}

    return 

@router.get("/get-item-transaction/{item_id}")
async def get_item_t():
    return