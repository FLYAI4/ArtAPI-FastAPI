import os
import json
import pytest
import pymongo
from datetime import datetime
from bson.binary import Binary
from pymongo.errors import ConnectionFailure


apps_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
conf_path = os.path.abspath(os.path.join(apps_path, "conf"))
img_path = os.path.abspath(os.path.join(apps_path, "img"))

conf_file = os.path.abspath(os.path.join(conf_path, "conf.json"))
with open(conf_file, "rt") as f:
    conf = json.load(f)
DB_NAME = conf["mongo"]["DB_NAME"]
COLLECTION_NAME = conf["mongo"]["COLLECTION_NAME"]

# MOCK data
USERNAME = "kim",
IMAGE_PATH = os.path.abspath(os.path.join(img_path, "test.jpg"))
ID = str(datetime.utcnow())


@pytest.fixture
def mockup():
    with open(IMAGE_PATH, "rb") as f:
        image_banary = Binary(f.read())
    yield {
        "_id": ID,
        "username": USERNAME,
        "image": image_banary
    }


@pytest.mark.asyncio
async def test_user_repository_can_insert_data_with_valid(mockup):
    # given : 유효한 데이터(사용자 정보 + 이미지 정보), 유효한 URL
    CONNECTION_URL = conf["mongo"]["CONNECTION_URL"]

    # when : DB에 데이터 저장
    client = pymongo.MongoClient(CONNECTION_URL)
    collection = client[DB_NAME][COLLECTION_NAME]
    result = collection.insert_one(mockup)

    # then : 이미지 ID 반환
    assert result.inserted_id == ID


@pytest.mark.asyncio
async def test_user_repository_cannot_insert_data_with_valid():
    # give : 잘못된 URL
    WRONG_URL = "wrong_url:!!"

    # when : DB에 데이터 저장 시 DB연결 오류
    # then : 에러
    with pytest.raises(Exception):
        client = pymongo.MongoClient(WRONG_URL)
        collection = client[DB_NAME][COLLECTION_NAME]
        result = collection.insert_one(mockup)

        # then : 이미지 ID 반환
        assert result.inserted_id == ID
