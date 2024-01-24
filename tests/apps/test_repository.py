import os
import pytest
from datetime import datetime
from bson.binary import Binary
from src.libs.db_manager import MongoManager
from src.apps.repository import Repository
from src.libs.exception import DBError


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


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_user_repository_can_insert_data_with_valid(mockup):
    # given : 유효한 데이터(사용자 정보 + 이미지 정보), 유효한 URL
    session = MongoManager().get_session()

    # when : DB에 데이터 저장
    result = Repository(session).insert_image(COLLECTION_NAME, mockup)

    # then : 이미지 ID 반환
    assert result.inserted_id == ID


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_user_repository_cannot_insert_data_with_invalid(mockup):
    # given : 동일한 ID를 가진 데이터, 유효한 URL
    session = MongoManager().get_session()

    # then : DBError
    with pytest.raises(DBError):
        # when : DB에 데이터 저장
        Repository(session).insert_image(COLLECTION_NAME, mockup)


@pytest.mark.asyncio
async def test_user_repository_cannot_insert_data_with_valid():
    # give : 잘못된 URL
    WRONG_URL = "wrong_url:!!"

    # then : DB 연결 오류
    with pytest.raises(DBError):
        # when : DB에 데이터 저장
        session = MongoManager(WRONG_URL).get_session()
        Repository(session).insert_image(COLLECTION_NAME, mockup)

