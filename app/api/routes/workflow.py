from fastapi import APIRouter

router = APIRouter()

@router.post("/workflow/")
async def run_workflow():
    return {"status": "workflow executed"}
