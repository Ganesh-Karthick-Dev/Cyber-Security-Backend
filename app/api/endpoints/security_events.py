from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import Optional, List
from app.api.endpoints.auth import oauth2_scheme
from app.utils.responses import APIResponse

router = APIRouter()


async def get_current_user_dependency(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from token"""
    from app.core.security import verify_token
    payload = verify_token(token)
    if payload is None:
        return None
    return payload.get("sub")


@router.get("/events")
async def get_security_events(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    severity: Optional[str] = Query(None, description="Filter by severity level"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: str = Depends(get_current_user_dependency)
):
    """
    Get security events with filtering and pagination
    Cyber security specific endpoint
    """
    if current_user is None:
        return APIResponse.unauthorized()
    
    # Demo security events data
    demo_events = [
        {
            "id": 1,
            "event_type": "login_attempt",
            "severity": "medium",
            "source_ip": "192.168.1.100",
            "user_agent": "Mozilla/5.0...",
            "timestamp": "2025-09-22T10:00:00Z",
            "description": "Failed login attempt",
            "status": "blocked"
        },
        {
            "id": 2,
            "event_type": "malware_detection",
            "severity": "high",
            "source_ip": "10.0.0.50",
            "file_hash": "abc123def456",
            "timestamp": "2025-09-22T09:30:00Z",
            "description": "Malware detected in uploaded file",
            "status": "quarantined"
        },
        {
            "id": 3,
            "event_type": "unauthorized_access",
            "severity": "critical",
            "source_ip": "203.0.113.1",
            "endpoint": "/admin/users",
            "timestamp": "2025-09-22T09:15:00Z",
            "description": "Unauthorized access attempt to admin panel",
            "status": "blocked"
        }
    ]
    
    # Apply filters
    filtered_events = demo_events
    if event_type:
        filtered_events = [e for e in filtered_events if e["event_type"] == event_type]
    if severity:
        filtered_events = [e for e in filtered_events if e["severity"] == severity]
    
    # Apply pagination
    paginated_events = filtered_events[skip:skip + limit]
    
    return APIResponse.success(
        data={
            "events": paginated_events,
            "total": len(filtered_events),
            "skip": skip,
            "limit": limit,
            "filters": {
                "event_type": event_type,
                "severity": severity
            }
        },
        message="Security events retrieved successfully"
    )


@router.get("/events/{event_id}")
async def get_security_event(
    event_id: int,
    current_user: str = Depends(get_current_user_dependency)
):
    """Get specific security event by ID"""
    if current_user is None:
        return APIResponse.unauthorized()
    
    # Demo event lookup
    if event_id == 1:
        event_data = {
            "id": 1,
            "event_type": "login_attempt",
            "severity": "medium",
            "source_ip": "192.168.1.100",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "timestamp": "2025-09-22T10:00:00Z",
            "description": "Failed login attempt for user 'admin'",
            "status": "blocked",
            "details": {
                "attempts": 3,
                "last_attempt": "2025-09-22T10:00:00Z",
                "username_attempted": "admin",
                "blocked_duration": "30 minutes"
            }
        }
        return APIResponse.success(data=event_data, message="Security event found")
    
    return APIResponse.not_found("Security event not found")


@router.get("/dashboard")
async def get_security_dashboard(
    current_user: str = Depends(get_current_user_dependency)
):
    """
    Get security dashboard metrics
    Cyber security dashboard endpoint
    """
    if current_user is None:
        return APIResponse.unauthorized()
    
    dashboard_data = {
        "summary": {
            "total_events_today": 15,
            "critical_events": 2,
            "high_events": 5,
            "medium_events": 6,
            "low_events": 2,
            "blocked_ips": 8,
            "quarantined_files": 3
        },
        "recent_events": [
            {
                "id": 1,
                "event_type": "unauthorized_access",
                "severity": "critical",
                "timestamp": "2025-09-22T11:30:00Z",
                "source_ip": "203.0.113.1"
            },
            {
                "id": 2,
                "event_type": "malware_detection",
                "severity": "high",
                "timestamp": "2025-09-22T11:15:00Z",
                "file_name": "suspicious.exe"
            }
        ],
        "threat_levels": {
            "current_threat_level": "medium",
            "last_updated": "2025-09-22T11:30:00Z",
            "trend": "stable"
        }
    }
    
    return APIResponse.success(
        data=dashboard_data,
        message="Security dashboard data retrieved successfully"
    )