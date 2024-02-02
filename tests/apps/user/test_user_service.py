import os
import pytest
from fastapi import FastAPI, UploadFile
from src.apps.user.service import UserService
from src.libs.db_manager import MongoManager

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# MOCK data
USERID = "user3@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))

app = FastAPI()


def test_user_service_can_save_image():
    with open(IMAGE_PATH, "rb") as f:
        img_file = UploadFile(file=f, filename="test.jpg")
        result = UserService.insert_image(USERID, img_file)

    print(result)
    assert result["generated_id"][-5:] == USERID[:5]


@pytest.mark.asyncio
async def test_user_business_can_generate_content_with_image():
    with open(IMAGE_PATH, "rb") as f:
        img_file = UploadFile(file=f, filename="test.jpg")
        result = UserService.insert_image(USERID, img_file)

        session = MongoManager().get_session()
        async for chunk in UserService.generate_content_with_image(session, result["generated_id"]):
            print(chunk)
