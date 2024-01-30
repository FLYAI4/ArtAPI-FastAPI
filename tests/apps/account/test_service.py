import pytest

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


@pytest.mark.asyncio
async def test_account_service_cannot_signup_user_with_existence_user():
    # given : 이미 가입된 Email

    # when : 중복된 Email 여부 확인

    # then : UserError 중복된 이메일
    pass


@pytest.mark.asyncio
async def test_account_service_cannot_signup_user_with_encrypt_error():
    # given : 유효한 사용자 정보

    # when : 비밀번호 암호화 요청

    # when : 중복된 Email 여부 확인

    # then : 중복되지 않은 Email 확인

    # then : 암호화 오류
    pass


@pytest.mark.asyncio
async def test_account_service_can_signup_user_with_valid(mockup):
    # given : 유효한 사용자 정보

    # when : 중복된 Email 여부 확인

    # then : 중복되지 않은 Email 확인

    # when : 비밀번호 암호화 요청

    # then : 암호화된 비밀번호

    # when : 정보 저장 요청

    # then : 사용자 EMAIL 반환
    pass
