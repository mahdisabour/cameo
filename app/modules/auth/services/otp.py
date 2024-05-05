from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

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

    @staticmethod
    async def get_by_options(
        db: Session,
        options: list = []
    ) -> OTPModel:
        return await OTPDAL(db=db).get_by_clause(
            clause=(select(OTPModel).where(
                *options
            ))
        )