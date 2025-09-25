from enum import Enum
from pydantic import BaseModel


class ScanTypeEnum(str, Enum):
    port = "port"
    version = "version"
    network = "network"
    server = "server"
    application = "application"
    database = "database"
    machine = "machine"


class ScanCreate(BaseModel):
    site_id: int
    type: ScanTypeEnum


class ScanOut(BaseModel):
    id: int
    site_id: int
    type: ScanTypeEnum
    status: str
    report_summary: str | None

    class Config:
        from_attributes = True


class ScanStatusOut(BaseModel):
    id: int
    status: str



