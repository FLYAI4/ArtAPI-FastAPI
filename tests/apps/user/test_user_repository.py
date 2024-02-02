import os
import pytest
from datetime import datetime
from bson.binary import Binary
from src.libs.api.util import generate_unique_id
from src.libs.api.exception import DBError
from src.libs.db_manager import MongoManager
from src.apps.user.repository import UserRepository
from src.apps.user.model import UserGeneratedInfo


user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# MOCK data
COLLECTION_NAME = "user_generated"
ID = "user2@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))
user_unique_id = generate_unique_id(ID)


@pytest.fixture
def mockup():
    with open(IMAGE_PATH, "rb") as f:
        origin_img = Binary(f.read())
    user_data = UserGeneratedInfo(origin_img=origin_img).model_dump()
    user_data["_id"] = user_unique_id
    yield user_data


@pytest.mark.order(1)
def test_user_repository_can_insert_data_with_valid(mockup):
    # given : 유효한 데이터(사용자 정보 + 이미지 정보), 유효한 URL
    session = MongoManager().get_session()

    # when : DB에 데이터 저장
    result = UserRepository.insert_image(session, mockup)
    # then : 이미지 ID 반환
    assert result == user_unique_id


# @pytest.mark.order(2)
# def test_user_repository_cannot_insert_data_with_invalid(mockup):
#     # given : 동일한 ID를 가진 데이터, 유효한 URL
#     session = MongoManager().get_session()

#     # then : DBError
#     with pytest.raises(DBError):
#         # when : DB에 데이터 저장
#         UserRepository.insert_image(session, COLLECTION_NAME, user_unique_id, mockup)


# def test_user_repository_cannot_insert_data_with_valid():
#     # give : 잘못된 URL
#     WRONG_URL = "wrong_url:!!"

#     # then : DB 연결 오류
#     with pytest.raises(DBError):
#         # when : DB에 데이터 저장
#         session = MongoManager(WRONG_URL).get_session()
#         UserRepository.insert_image(session, COLLECTION_NAME, user_unique_id, mockup)
