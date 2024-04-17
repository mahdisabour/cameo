from enum import Enum

from pydantic import BaseModel


class OrmModeBaseModel(BaseModel):
    class Config:
        orm_mode = True

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