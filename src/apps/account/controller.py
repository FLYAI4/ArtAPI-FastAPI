from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.libs.api.util import make_response
from src.libs.db_manager import PostgreManager
from src.apps.account.service import AccountService
from src.apps.account.schema import UserSignupPayload, UserLoginPayload

account = APIRouter(prefix="/account")


@account.post("/signup")
def user_signup(
    payload: UserSignupPayload,
    session: Session = Depends(PostgreManager().get_session)
):
    resp = AccountService.signup_user(session, payload)
    return make_response(resp)


@account.post("/login")
def user_login(
    payload: UserLoginPayload,
    session: Session = Depends(PostgreManager().get_session)
):
    resp = AccountService.login_user(session, payload)
    return make_response(resp)
