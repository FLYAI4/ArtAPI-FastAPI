import re
from sqlalchemy.orm import Session
from src.libs.api.exception import UserError
from src.libs.cipher import CipherManager
from src.libs.api.error_code import UserRequestErrorCode
from src.apps.account.repository import AccountRepository


class ApiValidator:
    def check_user_id_pattern(user_id: str):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, user_id):
            raise UserError(**UserRequestErrorCode.NonMatchEmail.value)

    def check_user_existence(session: Session, user_id: str):
        all_user_account = AccountRepository.get_all_user_account(session)
        if user_id in all_user_account:
            raise UserError(**UserRequestErrorCode.AlreadyUserError.value)

    def check_user_id(session: Session, user_id: str):
        all_user_account = AccountRepository.get_all_user_account(session)
        if user_id not in all_user_account:
            # then : UserError 반환
            raise UserError(**UserRequestErrorCode.NonSignupError.value)

    def check_user_password(session: Session,
                            encrypt_password: bytes,
                            user_password: str
                            ):
        origin_password = CipherManager().decrypt_password(encrypt_password)
        if user_password != origin_password:
            # then : UserError 반환
            raise UserError(**UserRequestErrorCode.WrongPasswordError.value)
