from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from app.core.config import get_settings
from app.db.session import get_session
from app.modules.auth.models.user.base_user import BaseUser
from app.modules.auth.schemas.user import TokenData
from app.modules.auth.dals.user.base_user import BaseUserDAL
from app.util.exceptions import AuthenticationFailed

SETTINGS = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=SETTINGS.PREFIX + "/auth" + "/users/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
) -> BaseUser:
    """
    This function checks authorization and if user has right to access returns its object

    .. note:: this function might raise `HTTPException` with code `401`
    """
    try:
        try:
            payload = jwt.decode(
                token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
            )
            username = payload.get("sub")
            if username is None:
                raise AuthenticationFailed()
            token_data = TokenData(username=username)
            if token_data.username is None:
                raise Exception()
        except ExpiredSignatureError:
            payload = jwt.decode(
                token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
            )
            raise AuthenticationFailed()
        except (JWTError, Exception):
            raise AuthenticationFailed()
        if (
            user := await BaseUserDAL(db=db).get_by_clause(
                clause=(select(BaseUser).where(username=token_data.username))
            )
        ) is None:
            raise AuthenticationFailed()
        return user
    finally:
        await db.close()