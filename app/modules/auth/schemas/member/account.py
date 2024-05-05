from enum import Enum
from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel, Field


class OrmModeBaseModel(BaseModel):
    class Config:
        from_attributes = True


class UserType(str, Enum):
    TALENT = "talent"
    USER = "user"


class RefreshToken(BaseModel):
    """
    Refresh Token schema
    """

    refresh_token: str


class Token(BaseModel):
    """
    Token schema (used at login)
    """

    access_token: str
    refresh_token: str
    expire: int
    token_type: str


class TokenData(BaseModel):
    """
    This schema represents data included in token
    """

    username: str | None = None


class AccountBaseSchema(OrmModeBaseModel):
    username: str
    email: str 
    date_of_birth: datetime
    phone_number: str | None = None
    name: str | None = None


class AccountCreateSchema(AccountBaseSchema):
    ...


class AccountGetSchema(AccountBaseSchema):
    id: str


class AccountUpdateSchema(AccountBaseSchema):
    ...


class AccountEmailStatus(BaseModel):
    account_id: str | None = None
    exist: bool = False


class CheckOTPPostSchema(BaseModel):
    otp: int
    email: str