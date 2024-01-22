import os
import pytest
from datetime import datetime
from bson.binary import Binary
from src.libs.db_manager import MongoManager


apps_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
img_path = os.path.abspath(os.path.join(apps_path, "img"))

# MOCK data
COLLECTION_NAME = "tests"
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
    db = MongoManager().get_session()

    # when : DB에 데이터 저장
    collection = db[COLLECTION_NAME]
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
        db = MongoManager(WRONG_URL).get_session()
        collection = db[COLLECTION_NAME]
        result = collection.insert_one(mockup)

        assert result.inserted_id == ID
