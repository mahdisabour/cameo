from datetime import timedelta

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.modules.auth.models.member.account import Account
from app.modules.auth.models.otp import OTPModel
from app.modules.auth.services.member.account import AccountRepository
from app.modules.auth.services.otp import OTPRepository
from app.modules.auth.services.member.user import UserRepository
from app.modules.auth.schemas.member.account import (
    AccountCreateSchema,
    AccountEmailStatus,
    Token
)
from app.modules.auth.schemas.otp import (
    CheckOTPPostSchema,
    OTPCreateSchema,
    OTPValidationSchema
)
from app.util.auth.jwt import (
    create_access_token,
    create_refresh_token
)
from app.core.config import get_settings
from app.db.session import get_session


SETTINGS = get_settings()
member_router = APIRouter(tags=["Member"], prefix="/members")


@member_router.get("/check-email", status_code=200, response_model=AccountEmailStatus)
async def email_status(
    email: str,
    db: Session = Depends(get_session),
):
    if (await AccountRepository.get_by_options(
        db=db,
        options=[Account.email == email]
    )):
        return AccountEmailStatus(
            exist=True,
        )
    return AccountEmailStatus()


@member_router.get("/request-OTP", status_code=200)
async def request_otp(
    email: str,
    db: Session = Depends(get_session)
):
    await OTPRepository.create_otp(
        db=db,
        otp_create_schema=OTPCreateSchema(
            account_email_fk=email
        )
    )


@member_router.post("/check-OTP", status_code=200, response_model=OTPValidationSchema)
async def check_otp(
    otp_data: CheckOTPPostSchema,
    db: Session = Depends(get_session),
):
    if (otp:= await OTPRepository.get_by_options(
            db=db,
            options=[
                OTPModel.otp_code==otp_data.otp,
                OTPModel.account_email_fk==otp_data.email
            ]
        )
    ):
        return otp
    return OTPValidationSchema(
        valid=False
    )
        
    


@member_router.post("/user/sign-up", status_code=201, response_model=Token)
async def register_user(
    data: AccountCreateSchema,
    db: Session = Depends(get_session),
):
    await UserRepository.create(
        db=db,
        data=data
    )
    # creating access and refresh token
    access_token_expires = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.email},
        expires_delta=access_token_expires,
    )
    refresh_token_expire = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES * 4)
    refresh_token = create_refresh_token(
        data={"sub": data.email},
        expires_delta=refresh_token_expire,
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expire=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        token_type="bearer",
    )