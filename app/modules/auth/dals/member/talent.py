from sqlalchemy.orm import Session

from app.util.crud.base import CRUDBase
from app.modules.auth.models.member.talent import TalentModel


class TalentDAL(CRUDBase[TalentModel, TalentModel, TalentModel]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=TalentModel)