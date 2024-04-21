from sqlalchemy.orm import Session

from app.util.crud.base import CRUDBase
from app.modules.auth.models.user.account import Account


class AccountDAL(CRUDBase[Account, Account, Account]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Account)