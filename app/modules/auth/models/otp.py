from datetime import datetime

from sqlalchemy import (
    String,
    DateTime
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from app.db.base_class import Base
from app.core.constant_variables import (
    STRING_LENGTH_32,
    STRING_LENGTH_64
)


class OTPModel(Base):
    __tablename__ = "otps"

    id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        primary_key=True
    )
    account_email_fk: Mapped[str] = mapped_column(
        ForeignKey("accounts.email", ondelete="CASCADE"),
    )
    otp_code: Mapped[int] = mapped_column()
    expiration_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
    )

    @hybrid_property
    def valid(self) -> bool:
        if self.expiration_time < datetime.now():
            return True
        return False

