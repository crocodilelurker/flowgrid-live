from database.Service_Models.Transaction_Service import Transaction_Model
from database.models import Transaction
from configurations import TransactionCollection,UserCollection
from services.UserServices import get_balance,get_user_id,get_items_list
from fastapi import Request, HTTPException
from bson import ObjectId
async def validate_transaction(transaction: Transaction_Model, request: Request):
    try:
        user_balance = await get_balance(request)
        print(f"User balance retrieved: {user_balance}")
    except Exception as e:
        #display the error
        print(f"Error retrieving user balance: {str(e)}")
    if transaction.transaction_type == "debit":
        if transaction.amount > user_balance:
            raise HTTPException(status_code=400, detail="Insufficient balance for debit transaction")
    elif transaction.transaction_type == "credit":
        if transaction.amount <= 0:
            raise HTTPException(status_code=400, detail="Credit amount must be greater than zero")
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")
    
async def update_transaction(transaction: Transaction_Model, request: Request):
    try:
        if(transaction.transaction_type == "debit"):
            receiver_id = transaction.receiver_id
            #receiver id is in str format, convert it to ObjectId
            receiver_id = ObjectId(receiver_id)
            receiver=await UserCollection.find_one({"_id": receiver_id})
            if not receiver:
                raise HTTPException(status_code=404, detail="Receiver not found")
            #update the receiver's balance
            result=await UserCollection.find_one_and_update(
                {"_id": receiver_id},
                {"$inc": {"balance": transaction.amount}}
            )
            #updating the sender's balance
            sender_id = await get_user_id(request)
            sender_id = ObjectId(sender_id)
            sender = await UserCollection.find_one({"_id": sender_id})
            if not sender:
                raise HTTPException(status_code=404, detail="Sender not found")
            #update the sender's balance
            await UserCollection.find_one_and_update(
                {"_id": sender_id},
                {"$inc": {"balance": -transaction.amount}}
            )
    except Exception as e:
        print(f"Error updating transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating transaction")

async def process_transaction(transaction: Transaction_Model, request: Request):
        try:
            print(f"Processing transaction:")
            #extraction of sender_id and receiver_id from the transaction
            sender_id = await get_user_id(request)
            receiver_id = transaction.receiver_id
            #create a transaction object with the Transaction Model
            transaction_data = Transaction(
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=transaction.amount,
                transaction_type=transaction.transaction_type
            )
            result = await TransactionCollection.insert_one(dict(transaction_data))
            print(f"Transaction created with ID: {str(result.inserted_id)}")
            return {"status_code": 201, "message": "Transaction created successfully", "transaction_id": str(result.inserted_id)}
        
        except Exception as e:
            print(f"Error processing transaction: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing transaction")
        
