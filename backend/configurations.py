from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://swagatsahu556:swagatsahu556@fg-0.vheqoan.mongodb.net/?retryWrites=true&w=majority&appName=FG-0"

def connectDB():
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

database= client['flowgrid']
UserCollection = database["Users"]
TransactionCollection = database["Transactions"]