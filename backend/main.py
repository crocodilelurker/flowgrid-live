from fastapi import FastAPI
from configurations import connectDB
from contextlib import asynccontextmanager
from routes.user_route import router as userRoutes
from routes.transaction_route import router as transactionRoutes
from routes.auth_route import router as authRoutes
@asynccontextmanager
async def lifespan(app: FastAPI):
    connectDB()
    yield
    print("Shutting down the application...")
app = FastAPI(lifespan=lifespan)
app.get("/")(lambda: {"message": "Welcome to FlowGrid Live! API"})

app.include_router(userRoutes)
app.include_router(transactionRoutes)
app.include_router(authRoutes)
