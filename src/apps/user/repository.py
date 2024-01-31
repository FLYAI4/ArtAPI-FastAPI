from src.libs.exception import DBError
from src.libs.error_code import DBErrorCode


class UserRepository:
    def insert_image(session, collection_name: str, img_data: dict) -> str:
        try:
            collection = session[collection_name]
            result_id = collection.insert_one(img_data)

            # TODO : 데이터가 들어가지 않는 경우가 존재!! connection pool setting 확인 필요
            return result_id
        except Exception as e:
            raise DBError(**DBErrorCode.DBProcessError.value, err=e)
