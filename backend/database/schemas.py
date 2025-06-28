def individual_user_details(user):
    return{
        "id": user["_id"],
        "username": user["username"],
        "email": user["email"],
        "balance": user["balance"],
        "items": user["items"],
    }
def individual_transaction_details(transaction):
    return {
        "id": transaction["_id"],
        "amount": transaction["amount"],
        "sender_id": transaction["sender_id"],
        "receiver_id": transaction["receiver_id"],
        "created_at": transaction["created_at"],
    }
def all_users_details(users):
    return [individual_user_details(user) for user in users]
def all_transactions_details(transactions):
    return [individual_transaction_details(transaction) for transaction in transactions]
