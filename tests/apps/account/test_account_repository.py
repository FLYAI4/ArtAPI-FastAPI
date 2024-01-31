import uuid
import pytest
import base64
from src.libs.db_manager import PostgreManager
from src.libs.api.exception import DBError
from src.apps.account.repository import AccountRepository

# Mock data
EMAIL = "test@naver.com"
PASSWORD = base64.b64encode(bytes("test1234", 'utf-8'))
NAME="별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def mockup():
    yield {
        "password": PASSWORD,
        "name": NAME,
        "gender": GENDER,
        "age": AGE
    }


@pytest.fixture
def session():
    yield PostgreManager().get_session()


def test_account_repository_can_insert_user_account(mockup, session):
    # given : 유효한 유저 정보
    unique_email = EMAIL + str(uuid.uuid4())[:10]
    mockup["email"] = unique_email

    # when : DB에 데이터 입력 요청
    result_email = AccountRepository.insert_user_account(session, mockup)

    # then : 입력완료되면 email 반환
    assert result_email == unique_email

    # then : 데이터 정상적으로 입력 되었는지 확인
    result = AccountRepository.get_user_account(session, result_email)

    assert result["email"] == unique_email
    assert result["password"] == PASSWORD
    assert result["name"] == NAME
    assert result["gender"] == GENDER
    assert result["age"] == AGE
    assert result["generate_count"] == 0
    assert result["status"]
    
    result = AccountRepository.delete_user_account(session, unique_email)
    assert result == unique_email



def test_account_repository_cannot_get_user_account(session):
    # given : DB에 없는 조회할 유저 ID
    WRONG_EMAIL = "wrong_email"
    # then : DBError
    with pytest.raises(DBError):
        AccountRepository.get_user_account(session, WRONG_EMAIL)

# TODO : update 부분 나중에 개발
# @pytest.mark.order(2)
# @pytest.mark.asyncio
# async def test_account_repository_can_update_user_account():
#     # given : 변경할 유저 정보

#     # when : DB에 데이터 변경 요청

#     # then : 변경된 데이터 확인
#     pass


def test_account_respository_can_get_all_user_account(session, mockup):
    # given : 생성된 계정 존재
    unique_email = EMAIL + str(uuid.uuid4())[:10]
    mockup["email"] = unique_email

    result_email = AccountRepository.insert_user_account(session, mockup)
    assert result_email == unique_email

    # when : DB에 데이터 전체 조회 요청
    result = AccountRepository.get_all_user_account(session)

    # then : 조회된 데이터 확인
    assert len(result) > 0
    assert unique_email in result

    result = AccountRepository.delete_user_account(session, unique_email)
    assert result == unique_email
