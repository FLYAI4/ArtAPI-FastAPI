from src.libs.exception import DBError
from src.libs.error_code import DBErrorCode


class Repository():
    def __init__(self, session: any) -> None:
        self.session = session

    def insert_image(self, collection_name: str, img_data: dict) -> str:
        try:
            collection = self.session[collection_name]
            result_id = collection.insert_one(img_data)
            if not result_id:
                raise Exception
            return result_id
        except Exception as e:
            DBError(**DBErrorCode.DBProcessError, err=e)
