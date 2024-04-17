from sqlalchemy import (
    String
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from app.db.base_class import Base
from app.core.constant_variables import (
    STRING_LENGTH_32,
    STRING_LENGTH_64
)
from app.modules.auth.models.user.base_user import BaseUser

class TalentModel(Base):
    __tablename__ = "talents"
    id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        primary_key=True
    )
    profile_id: Mapped[str] = mapped_column(
        ForeignKey("base_user.id", ondelete="SET NULL"),
        unique=True,
        nullable=False
    )
    profile: Mapped["BaseUser"] = relationship(back_populates="talent")