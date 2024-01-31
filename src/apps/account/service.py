from sqlalchemy.orm import Session
from src.apps.account.schema import UserSignupPayload, UserLoginPayload
from src.apps.account.repository import AccountRepository
from src.libs.cipher import CipherManager
from src.libs.api.validator import ApiValidator
from src.libs.token import TokenManager


class AccountService:
    def signup_user(session: Session, payload: UserSignupPayload):
        data = payload.model_dump()
        ApiValidator.check_user_existence(session, data["email"])

        # Encrypt password
        encrypt_password = CipherManager().encrypt_password(data["password"])
        data["password"] = encrypt_password

        result = AccountRepository.insert_user_account(session, data)
        return result

    def login_user(session: Session, payload: UserLoginPayload):
        data = payload.model_dump()

        # Validate ID, password
        ApiValidator.check_user_id(session, data["email"])
        user_info = AccountRepository.get_user_account(session, data["email"])
        ApiValidator.check_user_password(session,
                                         user_info["password"],
                                         data["password"])

        # Generate token
        token = TokenManager().create_token(user_info["email"])
        return {
            "email": user_info["email"],
            "token": token
        }
