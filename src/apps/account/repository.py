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
            with session:
                sql = select(Account).filter(Account.email == user_id)
                obj = session.execute(sql).scalar_one()
                # TODO : Login 개발할 때 status 여부 확인 -> USERERROR
                return {
                    "email": obj.email,
                    "password": obj.password,
                    "name": obj.name,
                    "gender": obj.gender,
                    "age": obj.age,
                    "generate_count": obj.generate_count,
                    "status": obj.status
                }
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)

    def get_all_user_account(session: Session):
        try:
            all_account_email = list()
            with session:
                sql = select(Account)
                for obj in session.execute(sql):
                    all_account_email.append(obj.Account.email)
            return all_account_email
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)

    def delete_user_account(session: Session, user_id: str):
        try:
            with session:
                sql = select(Account).filter(Account.email == user_id)
                obj = session.execute(sql).scalar_one()
                if obj:
                    session.delete(obj)
                session.commit()
            return user_id
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)
