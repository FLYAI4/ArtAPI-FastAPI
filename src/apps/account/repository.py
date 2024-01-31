from src.apps.account.model import Account
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.libs.api.exception import DBError
from src.libs.api.error_code import DBErrorCode


class AccountRepository:
    def insert_user_account(session: Session, user_account_data: dict):
        try:
            obj = Account(
                id=user_account_data["id"],
                password=user_account_data["password"],
                name=user_account_data["name"],
                gender=user_account_data["gender"],
                age=user_account_data["age"],
                )

            with session:
                session.add(obj)
                session.commit()
            return user_account_data["id"]
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)

    def get_user_account(session: Session, id: str):
        try:
            with session:
                sql = select(Account).filter(Account.id == id)
                obj = session.execute(sql).scalar_one()
                # TODO : Login 개발할 때 status 여부 확인 -> USERERROR
                return {
                    "id": obj.id,
                    "password": obj.password,
                    "name": obj.name,
                    "gender": obj.gender,
                    "age": obj.age,
                    "status": obj.status
                }
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)

    def get_all_user_account(session: Session):
        try:
            all_account_id = list()
            with session:
                sql = select(Account)
                for obj in session.execute(sql):
                    all_account_id.append(obj.Account.id)
            return all_account_id
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)

    def delete_user_account(session: Session, id: str):
        try:
            with session:
                sql = select(Account).filter(Account.id == id)
                obj = session.execute(sql).scalar_one()
                if obj:
                    session.delete(obj)
                session.commit()
            return id
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)
