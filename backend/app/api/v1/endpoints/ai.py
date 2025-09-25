from fastapi import APIRouter, Depends

from ....core.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/analyze")
async def ai_analyze(payload: dict, user=Depends(get_current_user)):
    return {"analysis": "stub", "input": payload}


@router.get("/recommendations/{site_id}")
async def ai_recommendations(site_id: int, user=Depends(get_current_user)):
    return {"site_id": site_id, "recommendations": []}


@router.post("/chat")
async def ai_chat(message: dict, user=Depends(get_current_user)):
    return {"reply": "AI assistant stub response."}



