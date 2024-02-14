import re
from sqlalchemy.orm import Session
from src.libs.api.exception import UserError
from src.libs.cipher import CipherManager
from src.libs.api.error_code import UserRequestErrorCode
from src.apps.account.repository import AccountRepository
from src.libs.token import TokenManager


class ApiValidator:
    def check_user_id_pattern(user_id: str):
        """Check ID is in email pattern."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, user_id):
            raise UserError(**UserRequestErrorCode.NonMatchEmail.value)

    def check_user_existence(session: Session, user_id: str):
        """Check user has already been created."""
        all_user_account = AccountRepository.get_all_user_account(session)
        if user_id in all_user_account:
            raise UserError(**UserRequestErrorCode.AlreadyUserError.value)

    def check_user_id(session: Session, user_id: str):
        """Check user is registed."""
        all_user_account = AccountRepository.get_all_user_account(session)
        if user_id not in all_user_account:
            raise UserError(**UserRequestErrorCode.NonSignupError.value)

    def check_user_password(session: Session,
                            encrypt_password: bytes,
                            user_password: str
                            ):
        """Check user password and the password stored in DB are the same."""
        origin_password = CipherManager().decrypt_password(encrypt_password)
        if user_password != origin_password:
            raise UserError(**UserRequestErrorCode.WrongPasswordError.value)

    def check_valid_token(id: str, token: str):
        """Check valid token."""
        if not token:
            raise UserError(**UserRequestErrorCode.NonTokenError.value)

        try:
            decode_token = TokenManager().decode_token(token)
            # unmatch id and token["id"]
            if id != decode_token["id"]:
                raise UserError(**UserRequestErrorCode.WrongTokenError.value)
        except Exception:
            raise UserError(**UserRequestErrorCode.WrongTokenError.value)