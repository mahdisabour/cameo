from enum import Enum

from pydantic import BaseModel


class OrmModeBaseModel(BaseModel):
    class Config:
        from_attributes = True


class UserType(str, Enum):
    TALENT = "talent"
    USER = "user"


class SocialMedia(str, Enum): 
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    YOUTUBE = "youtube"

class FollowerCount(str, Enum):
    sm_10k = "<10k"
    bt_10k_30k = "10k-30k"
    bt_30k_100k = "30k-100k"
    bt_100k_300k = "100k-300k"
    bt_300k_1m = "300k-1m"
    bt_1m_3m = "1m-3m"
    bt_3m_10m = "3m-10m"
    gt_10m = "+10m"


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