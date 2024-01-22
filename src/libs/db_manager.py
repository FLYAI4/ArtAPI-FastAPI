import pymongo
from . import conf
from .exception import DBConnectionError


class MongoManager:
    def __init__(self, url: str = conf["mongo"]["CONNECTION_URL"]) -> None:
        self.url = url
        self.db = conf["mongo"]["DB_NAME"]

    def get_session(self):
        try:
            self.client = pymongo.MongoClient(self.url)
            return self.client[self.db]
        except Exception as e:
            DBConnectionError(500, "Failed to connect Mongodb.", e)
