from pydantic import BaseModel

class Transaction_Model(BaseModel):
    amount: int
    transaction_type: str  # e.g., "credit", "debit"
    receiver_id: str