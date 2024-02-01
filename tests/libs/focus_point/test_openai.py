import os
import pytest
import base64
import requests
from dotenv import load_dotenv
from src.libs.focus_point.openai import FocusPointManager
from src.libs.api.exception import FocusPointError

load_dotenv()
focus_point_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(focus_point_path, "test_img"))
NO_TOKEN_ID_KEY = os.environ.get("OEPN_AI_NO_TOKEN_KEY", 'utf-8')
TOKEN_KEY = os.environ.get("OEPN_AI_TOKEN_KEY", 'utf-8')


# Mock data
IMG_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.fixture
def img_data():
    with open(IMG_PATH, "rb") as f:
        yield base64.b64encode(f.read()).decode('utf-8')


@pytest.mark.asyncio
async def test_cannot_content_and_coord_value_with_on_token(img_data):
    # given : 유효한 데이터(이미지) + 계정에 토큰이 없는 경우
    # when : 생성 요청
    # then : 토큰이 없는 경우 FocusPointError 발생
    with pytest.raises(FocusPointError):
        FocusPointManager(NO_TOKEN_ID_KEY).generate_content_and_coord(img_data)


@pytest.mark.asyncio
async def test_cannot_content_and_coord_value_with_no_image():
    # given : 빈 데이터 + 계정 토큰 존재
    # when : 생성 요청
    # then : 토큰이 없는 빈 데이터의 경우 FocusPointError 발생
    with pytest.raises(FocusPointError):
        FocusPointManager().generate_content_and_coord()


@pytest.mark.asyncio
async def test_can_generate_content_and_coord_value_with_valid(img_data):
    # given : 유효한 데이터(이미지)
    # when : 생성 요청
    result = FocusPointManager().generate_content_and_coord(img_data)
    # then : 정상 응답
    print(result)
    assert len(result) > 0

    # given : 정상 응답된 값

    # when : 값에서 해설 키워드/좌표 추출

    # then : 키워드/좌표/키워드 해설 추출
    pass
