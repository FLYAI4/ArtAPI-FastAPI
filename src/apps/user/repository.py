from src.libs.api.exception import DBError
from src.libs.api.error_code import DBErrorCode


class UserRepository:
    def insert_image(session, user_data: dict) -> str:
        try:
            collection = session["user_generated"]
            result_id = collection.insert_one(user_data)

            # TODO : 데이터가 들어가지 않는 경우가 존재!! connection pool setting 확인 필요
            return result_id.inserted_id
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)
