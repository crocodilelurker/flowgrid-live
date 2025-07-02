from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from configurations import connectDB
from contextlib import asynccontextmanager
from routes.user_route import router as userRoutes
from routes.transaction_route import router as transactionRoutes
from routes.auth_route import router as authRoutes
from routes.item_route import router as itemRoutes
@asynccontextmanager
async def lifespan(app: FastAPI):
    connectDB()
    yield
    print("Shutting down the application...")
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")
@app.get("/")
def home():
    return {"message": "Welcome to FlowGrid Live! API"}


app.include_router(userRoutes)
app.include_router(transactionRoutes)
app.include_router(itemRoutes)
app.include_router(authRoutes)

