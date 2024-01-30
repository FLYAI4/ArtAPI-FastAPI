import pytest
from src.libs.exception import UserError
from src.libs.error_code import UserRequestErrorCode
from src.libs.db_manager import PostgreManager
from src.apps.account.schema import UserSignupPayload
from src.apps.account.repository import AccountRepository
from src.apps.account.service import AccountService
from src.libs.cipher import CipherManager

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
async def test_account_service_cannot_login_with_no_signup_account(session):
    # given : 가입되지 않은 계정 로그인
    wrong_id = "wrong@naver.com"

    # when : 사용자 로그인 요청
    all_user_account = AccountRepository.get_all_user_account(session)
    with pytest.raises(UserError):
        if wrong_id not in all_user_account:
            # then : UserError 반환
            raise UserError(**UserRequestErrorCode.NonSignupError.value)


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_account_service_cannot_login_with_wrong_password(session):
    # given : 유효한 로그인 정보 + 잘못된 비밀번호
    wrong_password = "wrong1234"

    # when : 사용자 로그인 요청
    user_info = AccountRepository.get_user_account(session, EMAIL)
    assert user_info["email"] == EMAIL

    check_password = CipherManager().encrypt_password(PASSWORD)
    assert check_password == user_info["password"]

    with pytest.raises(UserError):
        origin_password = CipherManager().decrypt_password(user_info["password"])
        if wrong_password != origin_password:
            # then : UserError 반환
            raise UserError(**UserRequestErrorCode.WrongPasswordError.value)


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_account_service_can_login_with_valid(session):
    # given : 유효한 로그인 정보

    # when : 사용자 로그인 요청

    # when : token 생성
    
    # then : email, toeken 반환

    result = AccountRepository.delete_user_account(session, EMAIL)
    assert result == EMAIL
