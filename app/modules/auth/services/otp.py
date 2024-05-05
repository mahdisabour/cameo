from sqlalchemy.orm import Session

from app.modules.auth.models.otp import OTPModel
from app.modules.auth.schemas.otp import OTPCreateSchema
from app.modules.auth.dals.otp import OTPDAL

class OTPRepository:
    @staticmethod
    async def create_otp(
        db: Session,
        otp_create_schema: OTPCreateSchema
    ) -> None:
        await OTPDAL(db=db).create(
            obj_in=OTPModel(
                **otp_create_schema.model_dump()
            ),
            autocommit=True
        )