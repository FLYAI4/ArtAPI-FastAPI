import uuid
import pytest
from fastapi.testclient import TestClient
from src.apps import create_app
from src.apps.account.repository import AccountRepository
from src.libs.db_manager import PostgreManager


# Mock data
ID = "test@naver.com"
PASSWORD = "test1234"
NAME="별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def signup_mockup():
    yield {
        "password": PASSWORD,
        "name": NAME,
        "gender": GENDER,
        "age": AGE
    }


@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


@pytest.fixture
def session():
    yield PostgreManager().get_session()


def test_account_controller_can_signup_with_valid(client, session, signup_mockup):
    # given : 유효한 payload
    unique_id = ID + str(uuid.uuid4())[:10]
    signup_mockup["id"] = unique_id

    # when : 회원가입 요청
    response = client.post(
        "/account/signup",
        json=signup_mockup
    )

    # then : 정상 응답
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"] == unique_id

    # clean
    result = AccountRepository.delete_user_account(session, unique_id)
    assert result == unique_id


def test_account_controller_cannot_signup_with_invalid(client):
    # given : 유효하지 않은 payload(name 없이)
    wrong_data = {
        "id": ID,
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


def test_account_controller_can_login_with_valid(client, session, signup_mockup):
    # given : 유효한 payload
    unique_id = ID + str(uuid.uuid4())[:10]
    signup_mockup["id"] = unique_id

    response = client.post(
        "/account/signup",
        json=signup_mockup
    )

    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"

    # when : 로그인 요청
    login_mockup = {
        "id": unique_id,
        "password": PASSWORD
    }
    response = client.post(
        "/account/login",
        json=login_mockup
    )

    # then : 정상 응답
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["id"] == unique_id
    assert response.json()["data"]["token"]

    # clean
    result = AccountRepository.delete_user_account(session, unique_id)
    assert result == unique_id


def test_account_controller_cannot_login_with_invalid(client):
    # given : 유효하지 않은 payload(password 없이)
    wrong_data = {
        "id": ID
    }

    # when : 로그인 요청
    response = client.post(
        "/account/login",
        json=wrong_data
    )

    # then : 에러 응답(pydantic type error)
    assert response.status_code == 422
    assert response.json()["meta"]["message"] == "A required value is missing. Please check."
