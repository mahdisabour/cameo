from sqlalchemy.orm import Session

from app.util.crud.base import CRUDBase
from app.modules.auth.models.user.base_user import BaseUser


class BaseUserDAL(CRUDBase[BaseUser, BaseUser, BaseUser]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=BaseUser)