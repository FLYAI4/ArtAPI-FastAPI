from sqlalchemy.orm import Session
from src.apps.account.schema import UserSignupPayload, UserLoginPayload
from src.apps.account.repository import AccountRepository
from src.libs.cipher import CipherManager
from src.libs.api.validator import ApiValidator
from src.libs.token import TokenManager


class AccountService:
    def signup_user(session: Session, payload: UserSignupPayload):
        sign_data = payload.model_dump()
        ApiValidator.check_user_existence(session, sign_data["id"])

        # Encrypt password
        encrypt_password = CipherManager().encrypt_password(sign_data["password"])
        sign_data["password"] = encrypt_password

        result = AccountRepository.insert_user_account(session, sign_data)
        return result

    def login_user(session: Session, payload: UserLoginPayload):
        login_data = payload.model_dump()

        # Validate ID, password
        ApiValidator.check_user_id(session, login_data["id"])
        user_info = AccountRepository.get_user_account(session, login_data["id"])
        ApiValidator.check_user_password(session,
                                         user_info["password"],
                                         login_data["password"])

        # Generate token
        token = TokenManager().create_token(user_info["id"])
        return {
            "id": user_info["id"],
            "token": token
        }
