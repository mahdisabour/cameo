from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from app.modules.auth.models.member.account import Account
from app.modules.auth.dals.member.account import AccountDAL


class AccountRepository:
    @staticmethod
    async def get_by_options(
        db: Session,
        options: list = [],
    ) -> Account | None:
        account = await AccountDAL(db=db).get_by_clause(
            clause=(select(Account).where(
                *options
            ))
        )
        return account
