from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete

from ....core.dependencies import get_current_user
from ....db.database import get_session
from ....db.models import Site
from ....db.schemas import SiteCreate, SiteOut


router = APIRouter(prefix="/sites", tags=["sites"])


@router.post("", response_model=SiteOut, status_code=201)
async def add_site(payload: SiteCreate, user=Depends(get_current_user), session=Depends(get_session)):
    site = Site(owner_id=user.id, url=str(payload.url), label=payload.label)
    session.add(site)
    await session.commit()
    await session.refresh(site)
    return site


@router.get("", response_model=list[SiteOut])
async def list_sites(user=Depends(get_current_user), session=Depends(get_session)):
    res = await session.execute(select(Site).where(Site.owner_id == user.id))
    return list(res.scalars())


@router.delete("/{site_id}", status_code=204)
async def delete_site(site_id: int, user=Depends(get_current_user), session=Depends(get_session)):
    res = await session.execute(select(Site).where(Site.id == site_id, Site.owner_id == user.id))
    site = res.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    await session.execute(delete(Site).where(Site.id == site_id))
    await session.commit()
    return None



