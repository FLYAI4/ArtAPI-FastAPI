import pytest
from src.libs.exception import UserError
from src.libs.validator import ApiValidator
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
    mockup = mockup.model_dump()
    result = AccountRepository.insert_user_account(session, mockup)
    assert result == EMAIL

    # then : UserError 중복된 이메일
    with pytest.raises(UserError):
        # when : 중복된 Email 여부 확인
        ApiValidator.check_user_existence(session, mockup["email"])

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

    result = AccountRepository.delete_user_account(session, EMAIL)
    assert result == EMAIL
