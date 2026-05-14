from fastapi import APIRouter

router = APIRouter(tags=["root"])


@router.get("/")
def root():
    return {"message": "Welcome to the ResumeRadar API!."}
