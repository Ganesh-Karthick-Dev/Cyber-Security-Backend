from fastapi import APIRouter

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("")
async def get_plans():
    return [
        {"id": "free", "name": "Free", "price": 0, "limits": {"scans_per_month": 10}},
        {"id": "pro", "name": "Pro", "price": 29, "limits": {"scans_per_month": 500}},
        {"id": "enterprise", "name": "Enterprise", "price": 199, "limits": {"scans_per_month": 10000}},
    ]



