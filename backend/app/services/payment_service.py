from __future__ import annotations

from typing import Any
import stripe


class PaymentService:
    def __init__(self, stripe_secret_key: str | None):
        self.stripe_secret_key = stripe_secret_key
        if stripe_secret_key:
            stripe.api_key = stripe_secret_key

    async def create_subscription(self, user_id: int, plan_id: str) -> dict[str, Any]:
        return {"status": "created", "plan_id": plan_id}

    async def upgrade_subscription(self, user_id: int, plan_id: str) -> dict[str, Any]:
        return {"status": "upgraded", "plan_id": plan_id}

    async def billing_history(self, user_id: int) -> list[dict[str, Any]]:
        return []


