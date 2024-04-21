from sqlalchemy import (
    String
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base_class import Base
from app.core.constant_variables import (
    STRING_LENGTH_32,
    STRING_LENGTH_64
) 

class Category(Base):
    __tablename__ = "category"

    id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        primary_key=True
    )
    parent: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL"),
        nullable=True
    )
    name: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32)
    )