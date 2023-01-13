from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, validator

from core.seedwork.api_layer import qs_to_list


class OutputOrg(BaseModel):
    name: str
    id: int

    class Config:
        orm_mode = True


class OutputLegalRequirement(BaseModel):
    title: str
    id: int
    content: str
    accept_required: bool

    class Config:
        orm_mode = True


class OutputRegisterPage(BaseModel):
    orgs: list[OutputOrg]
    legal_requirements: list[OutputLegalRequirement]

    _ = qs_to_list("orgs")
    __ = qs_to_list("legal_requirements")

    class Config:
        orm_mode = True


class InputRlcUserCreate(BaseModel):
    org: int
    name: str
    email: EmailStr
    password: str
    password_confirm: str
    accepted_legal_requirements: list[int] = []

    @validator("password_confirm")
    def passwords_match(cls, v, values, **kwargs):
        if "password" not in values or "password" in values and v != values["password"]:
            raise ValueError("The passwords do not match.")
        return v


class OutputKey(BaseModel):
    id: int
    correct: bool
    source: Literal["RECORD", "ORG", "FOLDER", "USER"]
    information: str

    class Config:
        orm_mode = True


class InputKeyDelete(BaseModel):
    id: int


class InputUnlockOrgUser(BaseModel):
    id: int


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


class InputRlcUserGrantPermission(BaseModel):
    id: int
    permission: int


class InputRlcUserGet(BaseModel):
    id: int


class InputRlcUserActivate(BaseModel):
    id: int


class OutputRlcUserOptional(BaseModel):
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


class OutputRlcUserSmall(BaseModel):
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


class OutputRlcUser(BaseModel):
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


class OutputRlcUserData(BaseModel):
    user: OutputRlcUser
    rlc: Rlc
    badges: Badges
    permissions: List[str]
    settings: Optional[Dict]


class OutputStatisticsUser(BaseModel):
    id: int
    user_id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class OutputStatisticsUserData(BaseModel):
    user: OutputStatisticsUser
