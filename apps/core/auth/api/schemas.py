from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel


class Link(BaseModel):
    id: UUID
    name: str
    link: AnyUrl
    order: int

    class Config:
        orm_mode = True


class Rlc(BaseModel):
    id: int
    name: str
    use_record_pool: bool
    links: List[Link]

    class Config:
        orm_mode = True


class InputRlcUserUpdate(BaseModel):
    id: int
    name: Optional[str]
    birthday: Optional[Any]
    phone_number: Optional[str]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    speciality_of_study: Optional[str]
    note: Optional[str]


class InputRlcUserGet(BaseModel):
    id: int


class InputRlcUserActivate(BaseModel):
    id: int


class RlcUserOptional(BaseModel):
    id: int
    user_id: int
    birthday: Optional[Any]
    phone_number: Optional[str]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    locked: Optional[bool]
    locked_legal: Optional[bool]
    email_confirmed: Optional[bool]
    is_active: Optional[bool]
    accepted: Optional[bool]
    updated: Optional[datetime]
    note: Optional[str]
    name: Optional[str]
    email: Optional[str]
    created: Optional[datetime]
    speciality_of_study: Optional[str]
    speciality_of_study_display: Optional[str]

    class Config:
        orm_mode = True


class RlcUserSmall(BaseModel):
    id: int
    user_id: int
    phone_number: Optional[str]
    name: str
    email: str
    accepted: bool
    email_confirmed: bool
    locked: bool
    is_active: bool

    class Config:
        orm_mode = True


class RlcUser(BaseModel):
    id: int
    user_id: int
    birthday: Optional[Any]
    phone_number: Optional[str]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    locked: bool
    locked_legal: bool
    email_confirmed: bool
    is_active: bool
    accepted: bool
    updated: datetime
    note: Optional[str]
    name: str
    email: str
    created: datetime
    speciality_of_study: Optional[str]
    speciality_of_study_display: Optional[str]

    class Config:
        orm_mode = True


class Badges(BaseModel):
    profiles: int
    record_deletion_requests: int
    record_permit_requests: int
    legal: int


class RlcUserData(BaseModel):
    user: RlcUser
    rlc: Rlc
    badges: Badges
    permissions: List[str]
    settings: Optional[Dict]
