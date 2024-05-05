from random import randint
from uuid import uuid4
from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from app.core.config import get_settings

OTP_LEN = get_settings().OTP_LEN
range_start = 10**(OTP_LEN-1)
range_end = (10**OTP_LEN)-1


class OrmModeBaseModel(BaseModel):
    class Config:
        from_attributes = True


class OTPBaseSchema(OrmModeBaseModel):
    otp_code: int = Field(default_factory=lambda: randint(
        range_start, range_end
    ))
    account_email_fk: str


class OTPCreateSchema(OTPBaseSchema):
    id: str = Field(default_factory=lambda: uuid4().hex)
    expiration_time: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(seconds=get_settings().OTP_EXPIRATION_TIMEDELTA))