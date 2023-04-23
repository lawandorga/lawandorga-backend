import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from core.seedwork.api_layer import format_datetime, make_datetime_aware


class OutputRlc(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class OutputEventResponse(BaseModel):
    id: int
    created: datetime
    updated: datetime
    is_global: bool
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    org: OutputRlc
    level: str

    class Config:
        orm_mode = True

    _ = format_datetime("start_time")
    __ = format_datetime("end_time")


class InputEventCreate(BaseModel):
    name: str
    description: str = ""
    level: Literal["ORG", "META", "GLOBAL"]
    start_time: datetime
    end_time: datetime

    _ = make_datetime_aware("start_time")
    __ = make_datetime_aware("end_time")


class InputEventUpdate(BaseModel):
    id: int
    is_global: Optional[bool]
    name: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    _ = make_datetime_aware("start_time")
    __ = make_datetime_aware("end_time")


class InputEventDelete(BaseModel):
    id: int


class CalendarUuidUser(BaseModel):
    id: int
    calendar_uuid: uuid.UUID
    calendar_url: str
