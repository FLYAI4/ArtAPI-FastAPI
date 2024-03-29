import os
import pytest
import httpx
import time
from fastapi.testclient import TestClient
from src.apps import create_app
from src.apps.account.service import AccountService
from src.libs.db_manager import PostgreManager
from src.apps.account.schema import UserLoginPayload


# Mock data
user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

USERID = "kim@naver.com"
PASSWORD = "12312312"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.fixture
def client():
    app = create_app()
    client = TestClient(app)
    yield client


@pytest.fixture
def token():
    session = PostgreManager().get_session()
    payload = UserLoginPayload(id=USERID, password=PASSWORD)
    result = AccountService.login_user(session, payload)
    yield result["token"]
    


def test_user_can_insert_image(client, token):
    # given : 유효한 payload (header : username, file: UpladFile)
    headers = {"id": USERID, "token": token}

    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}

        # when : 콘텐츠 생성 API 요청
        response = client.post(
            "/user/image",
            headers=headers,
            files=files)

    # then : 정상 응답 username
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["generated_id"]


def test_user_cannot_insert_image_with_non_header(client):
    # given : 유효하지 않은 payload (header 없이 요청)
    # when : 콘텐츠 생성 API 요청
    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}

        # when : 콘텐츠 생성 API 요청
        response = client.post(
            "/user/image",
            files=files)
    assert response.status_code == 422
    assert response.json()["meta"]["message"] == "A required value is missing. Please check."


def test_user_cannot_insert_image_with_non_file(client):    
    # given : 유효하지 않은 payload (file 없이 요청)
    headers = {"id": USERID}

    # when : 콘텐츠 생성 API 요청
    response = client.post(
        "/user/image",
        headers=headers)

    # given : 에러메시지
    assert response.status_code == 422
    assert response.json()["meta"]["message"] == "A required value is missing. Please check."


@pytest.mark.asyncio
async def test_user_can_generate_content_with_image(client, token):
    start_time = time.time() # 시작 시간 측정

    # given : 유효한 payload (header : username, file: UpladFile)
    headers = {"id": USERID, "token": token}

    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}

        # when : 콘텐츠 생성 API 요청
        response = client.post(
            "/user/image",
            headers=headers,
            files=files)

    # then : 정상 응답 username
    assert response.status_code == 200

    # given : 유효한 generated_id
    generated_id = response.json()["data"]["generated_id"]
    body = {"generated_id": generated_id}

    app = create_app()
    # 콘텐츠 생성 API 요청
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac_client:
        response = await ac_client.post("/user/content",
                                        headers=headers,
                                        json=body)
        assert response.status_code == 200

        async for chunk in response.aiter_bytes():
            # 여기서 필요한 검증을 수행할 수 있음
            print(chunk)

    end_time = time.time()  # 끝난 시간 측정
    elapsed_time = end_time - start_time
    print()
    print("============== python ===============")
    print(f"테스트 함수 실행 시간: {elapsed_time} 초")
    print("=====================================")
