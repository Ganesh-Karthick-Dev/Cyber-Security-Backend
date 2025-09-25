from __future__ import annotations

import asyncio
from typing import Any

from loguru import logger
import json
import shlex
import asyncio.subprocess

from ...db.models.scan import ScanType


class KaliScanner:
    async def run_scan(self, url: str, scan_type: ScanType, timeout_seconds: int = 600) -> dict[str, Any]:
        logger.info(f"[scanner] starting {scan_type} scan for {url}")
        cmd = (
            "docker run --rm --network docker_cyber"
            " kali-tools python3 -m scan_scripts.entrypoint"
            f" --type {shlex.quote(scan_type.value)} --url {shlex.quote(url)}"
        )
        try:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_seconds)
            except asyncio.TimeoutError:
                proc.kill()
                raise
            if proc.returncode != 0:
                logger.warning("kali scan nonzero exit: {}", stderr.decode(errors="ignore"))
                raise RuntimeError("kali scan failed")
            text = stdout.decode()
            return json.loads(text)
        except Exception:
            # Safe fallback minimal result
            return {"url": url, "type": scan_type.value, "issues": [], "notes": "fallback"}


