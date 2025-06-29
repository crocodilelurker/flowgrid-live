from database.Service_Models.Transaction_Service import Transaction_Model
from database.models import Transaction
from configurations import TransactionCollection
from services.UserServices import get_balance,get_user_id
from fastapi import Request, HTTPException
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
async def process_transaction(transaction: Transaction_Model, request: Request):
    if transaction.transaction_type == "debit":
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
            
        except Exception as e:
            print(f"Error processing transaction: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing transaction")