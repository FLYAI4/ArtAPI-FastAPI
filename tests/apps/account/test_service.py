import pytest
from src.libs.exception import UserError
from src.libs.db_manager import PostgreManager
from src.apps.account.schema import UserSignupPayload
from src.apps.account.repository import AccountRepository
from src.apps.account.service import AccountService

# Mock data
EMAIL = "test@naver.com"
PASSWORD = "test1234"
NAME="별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def mockup():
    yield UserSignupPayload(
        email=EMAIL,
        password=PASSWORD,
        name=NAME,
        gender=GENDER,
        age=AGE
    )


@pytest.fixture
def session():
    yield PostgreManager().get_session()


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_account_service_cannot_signup_user_with_existence_user(mockup, session):
    # given : 이미 가입된 Email
    result = AccountService.signup_user(session, mockup)
    assert result == EMAIL

    # then : UserError 중복된 이메일
    with pytest.raises(UserError):
        # when : 중복된 Email 여부 확인
        AccountService.signup_user(session, mockup)

    result = AccountRepository.delete_user_account(session, EMAIL)
    assert result == EMAIL


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_account_service_can_signup_user_with_valid(mockup, session):
    # given : 유효한 사용자 정보
    # when : 사용자 회원가입 요청
    result = AccountService.signup_user(session, mockup)

    # then : 요청한 이메일 동일
    assert result == EMAIL


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_account_service_cannot_login_with_no_signup_account():
    # given : 가입되지 않은 계정 로그인
    
    # when : 사용자 로그인 요청
    
    # then : UserError 반환
    pass


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_account_service_cannot_login_with_wrong_password():
    # given : 유효한 로그인 정보 + 잘못된 비밀번호
    
    # when : 사용자 로그인 요청
    
    # then : UserError 반환
    pass


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_account_service_can_login_with_valid(session):
    # given : 유효한 로그인 정보

    # when : 사용자 로그인 요청

    # then : email, toeken 반환

    result = AccountRepository.delete_user_account(session, EMAIL)
    assert result == EMAIL
