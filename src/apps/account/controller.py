from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.libs.db_manager import PostgreManager
from src.apps.account.service import AccountService
from src.apps.account.schema import UserSignupPayload

account = APIRouter(prefix="/account")


@account.post("/signup")
def user_signup(
    payload: UserSignupPayload,
    session: Session = Depends(PostgreManager().get_session)
):
    resp = AccountService.signup_user(session, payload)
    return {
        "meta": {
            "code": 200,
            "message": "ok"
        },
        "data": resp
    }
