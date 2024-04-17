from sqlalchemy.orm import Session

from app.util.crud.base import CRUDBase
from app.modules.auth.models.user.user import UserModel


class TalentDAL(CRUDBase[UserModel, UserModel, UserModel]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=UserModel)