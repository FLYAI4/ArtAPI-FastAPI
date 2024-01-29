import pytest
from src.libs.db_manager import PostgreManager
from src.libs.exception import DBError
from src.apps.account.repository import AccountRepository


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
def session():
    yield PostgreManager().get_session()


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_account_repository_can_insert_user_account(mockup, session):
    # given : 유효한 유저 정보
    # when : DB에 데이터 입력 요청
    result_email = AccountRepository.insert_user_account(session, mockup)

    # then : 입력완료되면 email 반환
    assert result_email == EMAIL

    # then : 데이터 정상적으로 입력 되었는지 확인
    result = AccountRepository.get_user_account(session, result_email)

    assert result["email"] == EMAIL
    assert result["password"] == PASSWORD
    assert result["name"] == NAME
    assert result["gender"] == GENDER
    assert result["age"] == AGE
    assert result["generate_count"] == 0


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_account_repository_cannot_get_user_account(session):
    # given : DB에 없는 조회할 유저 ID
    WRONG_EMAIL = "wrong_email"
    # then : DBError
    with pytest.raises(DBError):
        AccountRepository.get_user_account(session, WRONG_EMAIL)


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_account_repository_can_update_user_account():
    # given : 변경할 유저 정보(ID제외)

    # when : DB에 데이터 변경 요청

    # then : 변경된 데이터 확인
    pass


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_account_respository_can_get_all_user_account():
    # given :

    # when : DB에 데이터 전체 조회 요청

    # then : 조회된 데이터 확인
    pass


@pytest.mark.asyncio(3)
async def test_account_repository_cannot_get_all_user_account():
    # given : 테이블에 아무 데이터도 없을 때

    # when : DB 데이터 조회 요청

    # then : 빈 리스트 출력
    pass
