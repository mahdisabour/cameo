from datetime import timedelta

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.modules.auth.services.member.account import AccountRepository
from app.modules.auth.services.otp import OTPRepository
from app.modules.auth.schemas.otp import OTPCreateSchema
from app.db.session import get_session

from app.modules.auth.schemas.member.account import (
    AccountEmailStatus,
    CheckOTPPostSchema
)


member_router = APIRouter(tags=["Member"], prefix="/members")


@member_router.get("/check-email", status_code=200, response_model=AccountEmailStatus)
async def email_status(
    email: str,
    db: Session = Depends(get_session),
):
    if (account := await AccountRepository.get_by_options(
        db=db,
        options={"email": email}
    )):
        return AccountEmailStatus(
            exist=True,
            account_id=account.id
        )
    return AccountEmailStatus()


@member_router.get("/request-OTP", status_code=200)
async def request_otp(
    account_id: str,
    db: Session = Depends(get_session)
):
    await OTPRepository.create_otp(
        db=db,
        otp_create_schema=OTPCreateSchema(
            account_id=account_id
        )
    )


@member_router.post("/check-OTP", status_code=200)
async def check_otp(
    otp_data: CheckOTPPostSchema,
    db: Session = Depends(get_session),
):
    pass
    


@member_router.post("/sign-up", status_code=201)
async def register_user(
    db: Session = Depends(get_session),
):
    pass