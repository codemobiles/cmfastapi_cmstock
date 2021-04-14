from fastapi import APIRouter, Depends
router = APIRouter()

@router.get("/")
def root():
    return {"iam": "transaction"}
