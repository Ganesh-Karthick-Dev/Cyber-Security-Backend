from __future__ import annotations

import asyncio
from typing import Any

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.database import async_session
from ...db.models.scan import Scan, ScanStatus
from ...db.models.site import Site
from .kali_scanner import KaliScanner
from .ai_analyzer import AIAnalyzer
from .report_generator import ReportGenerator


async def process_scan(scan_id: int) -> None:
    async with async_session() as session:  # type: AsyncSession
        res = await session.execute(select(Scan).where(Scan.id == scan_id))
        scan = res.scalar_one_or_none()
        if not scan:
            return

        scan.status = ScanStatus.RUNNING
        await session.commit()

        scanner = KaliScanner()
        analyzer = AIAnalyzer()
        reporter = ReportGenerator()

        try:
            site_res = await session.execute(select(Site).where(Site.id == scan.site_id))
            site = site_res.scalar_one_or_none()
            url = site.url if site else "http://example.com"
            scan_results: dict[str, Any] = await scanner.run_scan(url, scan.type)
            ai_findings = await analyzer.analyze(scan_results)
            summary = reporter.generate_summary(scan_results, ai_findings)

            scan.result = {"raw": scan_results, "ai": ai_findings}
            scan.report_summary = summary
            scan.status = ScanStatus.COMPLETED
            await session.commit()
        except Exception as exc:  # noqa: BLE001
            logger.exception("scan failed: {}", exc)
            scan.status = ScanStatus.FAILED
            await session.commit()


def kickoff_scan_async(scan_id: int) -> None:
    asyncio.create_task(process_scan(scan_id))


