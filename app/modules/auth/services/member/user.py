from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.auth.models.member.account import Account
from app.modules.auth.models.member.user import UserModel
from app.modules.auth.schemas.member.account import AccountCreateSchema
from app.modules.auth.dals.member.account import AccountDAL
from app.modules.auth.dals.member.user import UserDAL

class UserRepository:
    @staticmethod
    async def create(
        db: Session,
        data: AccountCreateSchema
    ) -> None:
        async with db.begin():
            account: Account = await AccountDAL(db=db).create(
                obj_in=Account(
                    id=str(uuid4().hex),
                    **data.model_dump()
                ),
                autocommit=False
            )
            await db.flush()
            
            _: UserModel = await UserDAL(db=db).create(
                obj_in=UserModel(
                    id=str(uuid4().hex),
                    account_id=account.id
                ),
                autocommit=False
            )

