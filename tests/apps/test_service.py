import os
import pytest
from fastapi import FastAPI, UploadFile, File
from fastapi.testclient import TestClient
from src.apps.service import Service
from src.libs.db_manager import MongoManager


apps_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
img_path = os.path.abspath(os.path.join(apps_path, "test_img"))

# MOCK data
USERNAME = "kim"
IMAGE_PATH = os.path.abspath(os.path.join(img_path, "test.jpg"))

app = FastAPI()


@app.post("/test/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    session = MongoManager().get_session()
    result = await Service(session).insert_image(USERNAME, file)
    return result


@pytest.mark.asyncio
async def test_user_service_can_insert_image_with_valid():
    client = TestClient(app)

    # given : 유효한 데이터(이미지)
    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        # when : DB에 저장
        response = client.post("/test/uploadfile/", files=files)

    # then : 정상 처리
    assert response.status_code == 200
    assert response.json()["username"] == USERNAME
