from sqlalchemy.orm import Session

from app.util.crud.base import CRUDBase
from app.modules.auth.schemas.otp import OTPCreateSchema
from app.modules.auth.models.otp import OTPModel

class OTPDAL(CRUDBase[OTPModel, OTPCreateSchema, OTPModel]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=OTPModel)