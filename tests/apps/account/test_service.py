import pytest
from src.libs.exception import UserError
from src.libs.db_manager import PostgreManager
from src.apps.account.schema import UserSignupPayload, UserLoginPayload
from src.apps.account.repository import AccountRepository
from src.apps.account.service import AccountService
from src.libs.token import TokenManager
from src.libs.validator import ApiValidator

# Mock data
EMAIL = "test@naver.com"
PASSWORD = "test1234"
NAME="별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def signupmockup():
    yield UserSignupPayload(
        email=EMAIL,
        password=PASSWORD,
        name=NAME,
        gender=GENDER,
        age=AGE
    )


@pytest.fixture
def loginmockup():
    yield UserLoginPayload(
        email=EMAIL,
        password=PASSWORD
    )


@pytest.fixture
def session():
    yield PostgreManager().get_session()


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_account_service_cannot_signup_user_with_existence_user(session, signupmockup):
    # given : 이미 가입된 Email
    result = AccountService.signup_user(session, signupmockup)
    assert result == EMAIL

    # then : UserError 중복된 이메일
    with pytest.raises(UserError):
        # when : 중복된 Email 여부 확인
        AccountService.signup_user(session, signupmockup)

    result = AccountRepository.delete_user_account(session, EMAIL)
    assert result == EMAIL


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_account_service_can_signup_user_with_valid(session, signupmockup):
    # given : 유효한 사용자 정보
    # when : 사용자 회원가입 요청
    result = AccountService.signup_user(session, signupmockup)

    # then : 요청한 이메일 동일
    assert result == EMAIL


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_account_service_cannot_login_with_no_signup_account(session):
    # given : 가입되지 않은 계정 로그인
    wrong_id = "wrong@naver.com"

    # when : 사용자 로그인 요청
    with pytest.raises(UserError):
        # then : UserError 반환
        ApiValidator.check_user_id(session, wrong_id)


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_account_service_cannot_login_with_wrong_password(session):
    # given : 유효한 로그인 정보 + 잘못된 비밀번호
    wrong_password = "wrong1234"

    # when : 사용자 로그인 요청
    user_info = AccountRepository.get_user_account(session, EMAIL)
    assert user_info["email"] == EMAIL

    # then : UserError 반환
    with pytest.raises(UserError):
        ApiValidator.check_user_password(session,
                                         user_info["password"],
                                         wrong_password)


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_account_service_can_login_with_valid(session, loginmockup):
    # given : 유효한 로그인 정보
    # when : token 생성
    result = AccountService.login_user(session, loginmockup)

    # then : token 값 확인
    decode_token = TokenManager().decode_token(result["token"])
    assert decode_token["email"] == result["email"]

    result = AccountRepository.delete_user_account(session, EMAIL)
    assert result == EMAIL
