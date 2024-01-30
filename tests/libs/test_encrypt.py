from src.libs.cipher import CipherManager

# Mock data
ORI_PASSWORD = "rlaalswns1234"


def test_can_encrypt_password_with_long_password():
    # given : 비정상적인 비밀번호(매우 긴 패스워드)
    long_password = ORI_PASSWORD * 10

    # when : 암호화
    encrypt_password = CipherManager().encrypt_password(long_password)

    # then : base64인코딩 + 암호화된 비밀번호
    assert isinstance(encrypt_password, bytes)

    # when : 복호화
    origin_password = CipherManager().decrypt_password(encrypt_password)

    # then : 비밀번호 동일 확인
    assert origin_password == long_password


def test_can_encrypt_password_with_short_password():
    # given : 비정상적인 비밀번호(매우 짧은 패스워드)
    short_password = "a"
    assert len(short_password) == 1

    encrypt_password = CipherManager().encrypt_password(short_password)

    # then : base64인코딩 + 암호화된 비밀번호
    assert isinstance(encrypt_password, bytes)

    # when : 복호화
    origin_password = CipherManager().decrypt_password(encrypt_password)

    # then : 비밀번호 동일 확인
    assert origin_password == short_password


def test_can_encrypt_password_with_special_charactors():
    special_password = "!!@@$^&*(*%$$%^&)"

    encrypt_password = CipherManager().encrypt_password(special_password)

    # then : base64인코딩 + 암호화된 비밀번호
    assert isinstance(encrypt_password, bytes)

    # when : 복호화
    origin_password = CipherManager().decrypt_password(encrypt_password)

    # then : 비밀번호 동일 확인
    assert origin_password == special_password


def test_can_encrypt_decrypt_password():
    # given : 정상적인 비밀번호
    # when : 암호화
    encrypt_password = CipherManager().encrypt_password(ORI_PASSWORD)

    # then : base64인코딩 + 암호화된 비밀번호
    assert isinstance(encrypt_password, bytes)

    # when : 복호화
    origin_password = CipherManager().decrypt_password(encrypt_password)

    # then : 비밀번호 동일 확인
    assert origin_password == ORI_PASSWORD
