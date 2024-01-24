import pymongo
from . import conf
from .exception import DBError
from .error_code import DBErrorCode


class MongoManager:
    def __init__(self, url: str = conf["mongo"]["CONNECTION_URL"]) -> None:
        self.url = url
        self.db = conf["mongo"]["DB_NAME"]

    def get_session(self) -> pymongo.MongoClient:
        try:
            self.client = pymongo.MongoClient(self.url)
            return self.client[self.db]
        except Exception as e:
            DBError(**DBErrorCode.DBConnectionError.value, err=e)
