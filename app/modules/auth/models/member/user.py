from sqlalchemy import (
    String,
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

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        primary_key=True
    )
    account_id: Mapped[str | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL"),
    )
    bio: Mapped[str | None] = mapped_column(
        String(STRING_LENGTH_64),
    )
    time_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    time_updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )
    account: Mapped["Account"] = relationship(back_populates="user")
