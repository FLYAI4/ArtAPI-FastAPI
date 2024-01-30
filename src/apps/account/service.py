from sqlalchemy.orm import Session
from src.apps.account.schema import UserSignupPayload
from src.apps.account.repository import AccountRepository
from src.libs.cipher import CipherManager
from src.libs.validator import ApiValidator


class AccountService:
    def signup_user(session: Session, payload: UserSignupPayload):
        data = payload.model_dump()
        ApiValidator.check_user_existence(session, data["email"])

        encrypt_password = CipherManager().encrypt_password(data["password"])

        data["password"] = encrypt_password
        result = AccountRepository.insert_user_account(session, data)
        return result
