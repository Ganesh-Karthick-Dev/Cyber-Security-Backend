from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select

from ....core.dependencies import get_current_user
from ....db.database import get_session
from ....db.models import Scan, ScanStatus, ScanType, Site
from ....db.schemas import ScanCreate, ScanOut, ScanStatusOut
from ....services.scanning.orchestrator import kickoff_scan_async


router = APIRouter(prefix="/scans", tags=["scans"])


@router.post("/start", response_model=list[ScanOut])
async def start_comprehensive_scan(site_id: int, background_tasks: BackgroundTasks, user=Depends(get_current_user), session=Depends(get_session)):
    res = await session.execute(select(Site).where(Site.id == site_id, Site.owner_id == user.id))
    site = res.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    scans: list[Scan] = []
    for stype in ScanType:
        scan = Scan(site_id=site.id, type=stype, status=ScanStatus.PENDING)
        session.add(scan)
        scans.append(scan)
    await session.commit()
    for s in scans:
        await session.refresh(s)
        background_tasks.add_task(kickoff_scan_async, s.id)
    return scans


@router.post("/start/{scan_type}", response_model=ScanOut)
async def start_specific_scan(scan_type: ScanType, payload: ScanCreate, background_tasks: BackgroundTasks, user=Depends(get_current_user), session=Depends(get_session)):
    res = await session.execute(select(Site).where(Site.id == payload.site_id, Site.owner_id == user.id))
    site = res.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    scan = Scan(site_id=site.id, type=scan_type, status=ScanStatus.PENDING)
    session.add(scan)
    await session.commit()
    await session.refresh(scan)
    background_tasks.add_task(kickoff_scan_async, scan.id)
    return scan


@router.get("/{scan_id}/status", response_model=ScanStatusOut)
async def get_scan_status(scan_id: int, user=Depends(get_current_user), session=Depends(get_session)):
    res = await session.execute(select(Scan).where(Scan.id == scan_id))
    scan = res.scalar_one_or_none()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return {"id": scan.id, "status": scan.status.value}


@router.get("/{site_id}/latest", response_model=ScanOut | None)
async def get_latest_report(site_id: int, user=Depends(get_current_user), session=Depends(get_session)):
    res = await session.execute(
        select(Scan).where(Scan.site_id == site_id).order_by(Scan.created_at.desc())
    )
    scan = res.scalars().first()
    return scan


@router.get("/{site_id}/history", response_model=list[ScanOut])
async def get_scan_history(site_id: int, user=Depends(get_current_user), session=Depends(get_session)):
    res = await session.execute(
        select(Scan).where(Scan.site_id == site_id).order_by(Scan.created_at.desc())
    )
    return list(res.scalars())


