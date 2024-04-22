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

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        primary_key=True
    )
    account_id: Mapped[str | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL"),
    )
    account: Mapped["Account"] = relationship(back_populates="user")
    bio: Mapped[str | None] = mapped_column(
        String(STRING_LENGTH_64),
    )
