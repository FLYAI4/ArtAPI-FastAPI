import pytest
from fastapi.testclient import TestClient
from src.apps import create_app
from src.apps.account.repository import AccountRepository
from src.libs.db_manager import PostgreManager


# Mock data
EMAIL = "test@naver.com"
PASSWORD = "test1234"
NAME="별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def mockup():
    yield {
        "email": EMAIL,
        "password": PASSWORD,
        "name": NAME,
        "gender": GENDER,
        "age": AGE
    }
    
@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


@pytest.mark.asyncio
async def test_account_controller_can_signup_with_valid(client, mockup):
    # given : 유효한 payload
    # when : 회원가입 요청
    response = client.post(
        "/account/signup",
        json=mockup
    )

    # then : 정상 응답
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"] == EMAIL

    AccountRepository.delete_user_account(PostgreManager().get_session(), EMAIL)


@pytest.mark.asyncio
async def test_account_controller_cannot_signup_with_invalid(client):
    # given : 유효하지 않은 payload(name 없이)
    wrong_data = {
        "email": EMAIL,
        "password": PASSWORD,
        "gender": GENDER,
        "age": AGE
    }

    # when : 회원가입 요청
    response = client.post(
        "/account/signup",
        json=wrong_data
    )

    # then : 에러 응답(pydantic type error)
    assert response.status_code == 422
    assert response.json()["meta"]["message"] == "A required value is missing. Please check."
