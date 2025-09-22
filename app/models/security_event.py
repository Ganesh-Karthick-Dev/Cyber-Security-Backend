from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Enum
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class EventSeverity(str, enum.Enum):
    """Event severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventStatus(str, enum.Enum):
    """Event status types"""
    ACTIVE = "active"
    BLOCKED = "blocked"
    RESOLVED = "resolved"
    INVESTIGATING = "investigating"
    QUARANTINED = "quarantined"


class SecurityEvent(Base):
    """
    Security Event model for cyber security incidents
    Tracks various security events like login attempts, malware, etc.
    """
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), index=True, nullable=False)  # login_attempt, malware_detection, etc.
    severity = Column(Enum(EventSeverity), default=EventSeverity.MEDIUM, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.ACTIVE, nullable=False)
    
    # Event details
    source_ip = Column(String(45), index=True, nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    endpoint = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    
    # Additional data stored as JSON
    metadata = Column(JSON, nullable=True)  # Store additional event-specific data
    
    # File-related fields (for malware detection, etc.)
    file_hash = Column(String(64), nullable=True)  # SHA256 hash
    file_name = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<SecurityEvent(type='{self.event_type}', severity='{self.severity}', ip='{self.source_ip}')>"