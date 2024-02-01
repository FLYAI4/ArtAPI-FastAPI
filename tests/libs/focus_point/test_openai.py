import os
import pytest
import base64
import requests
from dotenv import load_dotenv

load_dotenv()
focus_point_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(focus_point_path, "test_img"))
NO_TOKEN_ID_KEY = os.environ.get("OEPN_AI_NO_TOKEN_KEY", 'utf-8')
TOKEN_KEY = os.environ.get("OEPN_AI_TOKEN_KEY", 'utf-8')


# Mock data
IMG_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.fixture
def headers():
    yield {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN_KEY}"
    }

@pytest.fixture
def payload():
    with open(IMG_PATH, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode('utf-8')

    yield {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert art historian with vast knowledge about artists throughout history who revolutionized their craft. You will begin by briefly summarizing the personal life and achievements of the artist. Then you will go on to explain the medium, style, and influences of their works. Then you will provide short descriptions of what they depict and any notable characteristics they might have. Fianlly identify THREE keywords in the picture and provide each coordinate of the keywords in the last sentence. For example if the keyword is woman, the output must be 'woman':[[x0,y0,x1,y1]] ",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 800
    }


@pytest.mark.asyncio
async def test_cannot_content_and_coord_value_with_on_token(payload):
    # given : 유효한 데이터(이미지) + 계정에 토큰이 없는 경우
    wrong_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NO_TOKEN_ID_KEY}"
    }

    # when : 생성 요청
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=wrong_headers,
                             json=payload)

    # then : 토큰이 없는 경우 mode_not_found 404 error 발생
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "model_not_found"


@pytest.mark.asyncio
async def test_cannot_content_and_coord_value_with_no_image(headers):
    # given : 빈 데이터 + 계정 토큰 존재
    wrong_payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert art historian with vast knowledge about artists throughout history who revolutionized their craft. You will begin by briefly summarizing the personal life and achievements of the artist. Then you will go on to explain the medium, style, and influences of their works. Then you will provide short descriptions of what they depict and any notable characteristics they might have. Fianlly identify THREE keywords in the picture and provide each coordinate of the keywords in the last sentence. For example if the keyword is woman, the output must be 'woman':[[x0,y0,x1,y1]] ",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,"   # 빈값 전달
                        }
                    }
                ]
            }
        ],
        "max_tokens": 800
    }

    # when : 생성 요청
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers,
                             json=wrong_payload)

    # then : 비정상 응답
    assert response.status_code == 400
    assert not response.json()["error"]["code"]
    assert response.json()["error"]["message"] == 'Invalid base64 image_url.'


@pytest.mark.asyncio
async def test_can_generate_content_and_coord_value_with_valid(headers, payload):
    # given : 유효한 데이터(이미지)
    # when : 생성 요청
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers,
                             json=payload)
    # then : 정상 응답
    assert response.status_code == 200
    assert response.json()["object"] == "chat.completion"
    assert len(response.json()['choices'][0]["message"]["content"]) > 0

    # given : 정상 응답된 값

    # when : 값에서 해설 키워드/좌표 추출

    # then : 키워드/좌표/키워드 해설 추출
    pass
