from fastapi import APIRouter

router= APIRouter(prefix="/item",tags="Items")

router.get("/")
async def rot():
    return {
        "message":"Welcome to FlowGrid Items API"
    }