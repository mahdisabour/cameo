from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_session
from app.modules.auth.models.user.user import UserModel
from app.modules.auth.schemas.user import TokenData
from app.modules.auth.services.user import UserRepository
from app.util.exceptions import AuthenticationFailed

SETTINGS = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=SETTINGS.PREFIX + "/auth" + "/users/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
) -> UserModel:
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
            session_id = payload.get("s_id")
            if username is None:
                raise AuthenticationFailed()
            token_data = TokenData(username=username)
            if token_data.username is None:
                raise Exception()
        except ExpiredSignatureError:
            payload = jwt.decode(
                token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
            )
            session_id = payload.get("s_id")
            await UserRepository.remove_session(db=db, session_id=session_id)
            raise AuthenticationFailed()
        except (JWTError, Exception):
            raise AuthenticationFailed()
        if (await UserRepository.get_session(session_id=session_id, db=db)) is None:
            raise AuthenticationFailed()
        if (
            user := await UserRepository.get_user(username=token_data.username, db=db)
        ) is None:
            raise AuthenticationFailed()
        # TODO: update user session here and change state to online
        return user
    finally:
        await db.close()