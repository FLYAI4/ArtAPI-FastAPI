from sqlalchemy.orm import Session
from src.libs.exception import UserError
from src.libs.error_code import UserRequestErrorCode
from src.apps.account.repository import AccountRepository


class ApiValidator:
    def check_user_existence(session: Session, user_id: str):
        all_user_account = AccountRepository.get_all_user_account(session)
        if user_id in all_user_account:
            raise UserError(**UserRequestErrorCode.AlreadyUserError.value)
