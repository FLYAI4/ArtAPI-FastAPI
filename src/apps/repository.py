from src.libs.exception import DBProcessError


class Repository():
    def __init__(self, session: any) -> None:
        self.session = session

    def insert_image(self, collection_name: str, img_data: dict) -> str:
        try:
            collection = self.session[collection_name]
            result_id = collection.insert_one(img_data)
            return result_id
        except Exception as e:
            DBProcessError(500, "Failed to insert data", e)
