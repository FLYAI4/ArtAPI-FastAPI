import os
import json
import pytest
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Mock data
ORI_PASSWORD = "rlaalswns1234"

libs_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
tests_path = os.path.abspath(os.path.join(libs_path, os.path.pardir))
apps_path = os.path.abspath(os.path.join(tests_path, 'apps'))
conf_path = os.path.abspath(os.path.join(apps_path, 'conf'))
conf_file = os.path.abspath(os.path.join(conf_path, 'conf.json'))

with open(conf_file, "rt") as f:
    conf = json.load(f)

dek = bytes(conf["ecryption_key"], 'utf-8')
BLOCK_SIZE = 16
aes = AES.new(dek, AES.MODE_ECB)


@pytest.mark.asyncio
async def test_can_encrypt_password_with_long_password():
    # given : 비정상적인 비밀번호(매우 긴 패스워드)
    long_password = ORI_PASSWORD * 10
    assert len(long_password) > 100

    encoding_password = pad(long_password.encode(), BLOCK_SIZE)

    # when : 암호화
    encrypt_password = aes.encrypt(encoding_password)
    base64_password = base64.b64encode(encrypt_password)

    # then : base64인코딩 + 암호화된 비밀번호
    assert isinstance(base64_password, bytes)

    # when : 복호화
    decrypt_password = aes.decrypt(base64.b64decode(base64_password))
    origin_password = unpad(decrypt_password, BLOCK_SIZE).decode()

    # then : 비밀번호 동일 확인
    assert origin_password == long_password


@pytest.mark.asyncio
async def test_can_encrypt_password_with_short_password():
    # given : 비정상적인 비밀번호(매우 짧은 패스워드)
    short_password = "a"
    assert len(short_password) == 1

    encoding_password = pad(short_password.encode(), BLOCK_SIZE)

    # when : 암호화
    encrypt_password = aes.encrypt(encoding_password)
    base64_password = base64.b64encode(encrypt_password)

    # then : base64인코딩 + 암호화된 비밀번호
    assert isinstance(base64_password, bytes)

    # when : 복호화
    decrypt_password = aes.decrypt(base64.b64decode(base64_password))
    origin_password = unpad(decrypt_password, BLOCK_SIZE).decode()

    # then : 비밀번호 동일 확인
    assert origin_password == short_password


@pytest.mark.asyncio
async def test_can_encrypt_decrypt_password():
    # given : 정상적인 비밀번호
    encoding_password = pad(ORI_PASSWORD.encode(), BLOCK_SIZE)

    # when : 암호화
    encrypt_password = aes.encrypt(encoding_password)
    base64_password = base64.b64encode(encrypt_password)

    # then : base64인코딩 + 암호화된 비밀번호
    assert isinstance(base64_password, bytes)

    # when : 복호화
    decrypt_password = aes.decrypt(base64.b64decode(base64_password))
    origin_password = unpad(decrypt_password, BLOCK_SIZE).decode()

    # then : 비밀번호 동일 확인
    assert origin_password == ORI_PASSWORD
