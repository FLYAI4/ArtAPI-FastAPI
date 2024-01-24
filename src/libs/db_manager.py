import os
import pymongo
from .exception import DBError
from .error_code import DBErrorCode


class MongoManager:
    def __init__(
        self, url: str = os.environ.get('MONGO_CONNECTION_URL')
    ) -> None:
        self.url = url
        self.db = os.environ.get('DB_NAME')

    def get_session(self) -> pymongo.MongoClient:
        if not self.url:
            raise Exception("No url")

        try:
            self.client = pymongo.MongoClient(self.url)
            return self.client[self.db]
        except Exception as e:
            raise DBError(**DBErrorCode.DBConnectionError.value, err=e)
