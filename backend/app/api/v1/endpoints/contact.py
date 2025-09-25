from fastapi import APIRouter, status

router = APIRouter(prefix="/contact", tags=["support"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def contact_support(message: dict):
    return {"received": True}



