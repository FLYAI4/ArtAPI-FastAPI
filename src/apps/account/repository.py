from src.apps.account.model import Account
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.libs.exception import DBError
from src.libs.error_code import DBErrorCode


class AccountRepository:
    def insert_user_account(session: Session, user_account_data: dict):
        try:
            obj = Account(
                email=user_account_data["email"],
                password=user_account_data["password"],
                name=user_account_data["name"],
                gender=user_account_data["gender"],
                age=user_account_data["age"],
                generate_count=0
                )

            with session:
                session.add(obj)
                session.commit()
            return user_account_data["email"]
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)

    def get_user_account(session: Session, user_id: str):
        try:
            sql = select(Account).filter(Account.email == user_id)
            obj = session.execute(sql).scalar_one()
            return {
                "email": obj.email,
                "password": obj.password,
                "name": obj.name,
                "gender": obj.gender,
                "age": obj.age,
                "generate_count": obj.generate_count
            }
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)
