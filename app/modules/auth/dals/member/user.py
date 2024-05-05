from sqlalchemy.orm import Session

from app.util.crud.base import CRUDBase
from app.modules.auth.models.member.user import UserModel


class UserDAL(CRUDBase[UserModel, UserModel, UserModel]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=UserModel)