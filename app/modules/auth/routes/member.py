from datetime import timedelta

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


member_router = APIRouter(tags=["Member"], prefix="/members")