from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import JSON, DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..database import Base


class ScanType(str, Enum):
    PORT = "port"
    VERSION = "version"
    NETWORK = "network"
    SERVER = "server"
    APPLICATION = "application"
    DATABASE = "database"
    MACHINE = "machine"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    type: Mapped[ScanType] = mapped_column(SqlEnum(ScanType), index=True)
    status: Mapped[ScanStatus] = mapped_column(SqlEnum(ScanStatus), default=ScanStatus.PENDING, index=True)
    result: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    report_summary: Mapped[Optional[str]] = mapped_column(String(4096), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    site = relationship("Site")



