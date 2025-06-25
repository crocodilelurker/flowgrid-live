from fastapi import APIRouter
from fastapi import FastAPI
from configurations import connectDB
from contextlib import asynccontextmanager
from routes.route import router
from database.models import User, Transaction
from configurations import UserCollection, TransactionCollection
@asynccontextmanager
async def lifespan(app: FastAPI):
    connectDB()
    yield
    print("Shutting down the application...")
app = FastAPI(lifespan=lifespan)

app.include_router(router)
