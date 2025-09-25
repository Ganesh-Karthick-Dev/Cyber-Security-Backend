from fastapi import APIRouter, Depends

from ....core.config import get_settings
from ....core.dependencies import get_current_user
from ....services.payment_service import PaymentService


router = APIRouter(prefix="/subscriptions", tags=["billing"])


@router.post("/create")
async def create_subscription(plan_id: str, user=Depends(get_current_user)):
    service = PaymentService(get_settings().stripe_secret_key)
    return await service.create_subscription(user.id, plan_id)


@router.post("/upgrade")
async def upgrade_subscription(plan_id: str, user=Depends(get_current_user)):
    service = PaymentService(get_settings().stripe_secret_key)
    return await service.upgrade_subscription(user.id, plan_id)


@router.get("/billing/history")
async def billing_history(user=Depends(get_current_user)):
    service = PaymentService(get_settings().stripe_secret_key)
    return await service.billing_history(user.id)



