from fastapi import APIRouter
from database.models import Transaction
from configurations import TransactionCollection
from bson import ObjectId

router = APIRouter(prefix="/transactions", tags=["Transactions"])
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live! Transaction API"}
@router.post("/create-transaction")
async def create_transaction(transaction: Transaction):
    try:
        result = await TransactionCollection.insert_one(dict(transaction))
        return {"status_code": 201, "message": "Transaction created successfully", "transaction_id": str(result.inserted_id)}
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
async def get_transaction(transaction_id: str):
    try:
        transaction = await TransactionCollection.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            return {"status_code": 200, "message": "Transaction found", "transaction": convert_object_id_to_str(transaction)}
        else:
            return {"status_code": 404, "message": "Transaction not found"}
    except Exception as e:
        return {"status_code": 500, "message": "Error retrieving transaction", "error": str(e)}