from fastapi import APIRouter

router= APIRouter(prefix="/item",tags=["Items"])
@router.get("/")
def root():
    return {"message": "Welcome to FlowGrid Live! Items API"}