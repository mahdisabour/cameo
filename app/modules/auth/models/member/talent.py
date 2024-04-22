from sqlalchemy import (
    Column,
    String,
    Enum,
    DateTime
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import func

from app.db.base_class import Base
from app.core.constant_variables import (
    STRING_LENGTH_32,
    STRING_LENGTH_64
)
from app.modules.auth.models.member.account import Account
from app.modules.auth.schemas.member.user import (
    UserType, 
    SocialMedia,
    FollowerCount
)

class TalentModel(Base):
    __tablename__ = "talents"
    id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        primary_key=True
    )
    user_type: Mapped[UserType] = mapped_column(
        default=UserType.USER, 
    )
    account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL"),
        unique=True,
    )
    account: Mapped["Account"] = relationship(back_populates="talent")
    legal_name: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
    )
    display_name: Mapped[str | None] = mapped_column(
        String(STRING_LENGTH_32),
    )
    date_of_birth: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    country: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
    )
    largest_social_media: Mapped[SocialMedia]
    social_media_id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32)
    )
    largest_following: Mapped[FollowerCount]
    referal_code: Mapped[str | None]    
    description: Mapped[str | None] = mapped_column(
        String(STRING_LENGTH_64)
    )

