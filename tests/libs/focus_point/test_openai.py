import os
import pytest
import base64
import re
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
async def test_cannot_content_and_coord_with_no_coord():
    # given : 잘못된 데이터(좌표 값이 없는)
    wrong_content = """
Unfortunately, without the name or context of a particular artist, I am unable to provide a factual biography or discuss their personal achievements. However, I can still discuss the image provided in terms of its visual elements and style.

This painting is done in a highly stylized manner, with vibrant colors and exaggerated features that are reminiscent of Naïve or Folk Art styles. The bright, solid colors and the flattened perspective create a sense of whimsy and simplicity. There's a clear influence of pastoral and landscape traditions, yet with a modern twist in the way the natural elements are depicted with a surreal quality.

The image depicts a lush, rolling landscape with terraced fields, perhaps tea fields or rice paddies, which suggests an East Asian setting. There are trees distributed in a way that complements the curves of the land. In the distance, a winding river leads towards a calm, blue lake, surrounded by layered hills or mountains, emphasizing the depth of the scene. Hot air balloons float gently in the sky, adding a playful and fantastic element to the scene. A small red brick structure on the left adds a hint of human presence without overtaking the natural beauty of the scene.

Considering the elements in this image, here are three keywords with their respective coordinates:
"""
    # when : 파싱 요청
    all_coords = extract_coord_keyword(wrong_content)
    # then : 빈 딕셔너리 응답
    assert not all_coords


def concat_content_coord(content: str, coord_dict: dict):
    # 설명 정제
    keyword = ':'
    if keyword in content:
        content = content[:content.find(keyword)].strip()
    content = content.replace("\n", " ").strip()
    print(content)

    response = {}
    for key, item in coord_dict.items():
        response[key] = {"coord": item, "context": ""}
    # print(response)

    for sentence in list(content.split('. ')):
        for key in coord_dict.keys():
            if key in sentence:
                response[key]["context"] += sentence + ". "
    return response


def extract_coord_keyword(content: str):
    # TODO : 좌표 추출 오류 수정
    # TODO : 좌표 추출 코드 수정
    import json
    pattern = r'```json(.*?)```'
    json_data = re.search(pattern, content, re.DOTALL)
    data_dict = {}
    if json_data:
        json_string = json_data.group(1).strip()

        # JSON 문자열을 딕셔너리로 파싱
        data_dict = json.loads(json_string)

    return data_dict


@pytest.mark.asyncio
async def test_can_extract_word():
    # given 유효한 데이터
    content = """
The artwork displayed is an idyllic landscape painting that appears to employ a stylized realism. The medium looks like it could be acrylic or oil on canvas, given the vibrancy of the colors and the smooth texture of the painted surface. The style presents a harmonized composition with vibrant colors, and there's a certain rhythm created by the patterns of the fields. This style is reminiscent of folk art or naive art, which often features simplified forms and a sense of serenity.

The painting depicts a lush green landscape with a meandering river leading towards a tranquil blue lake. Terraced fields, perhaps indicative of rice paddies or tea plantations, add a patterned texture to the rolling hills. Trees intermittently dot the landscape, and the presence of hot air balloons in the sky introduces a whimsical or fantastical element to the scene. There's a structure visible to the left, possibly part of a house or an outbuilding with a red brick chimney and a white parasol, suggesting a human presence without showing actual figures.

Now, for the coordinates of three keywords within the image:

1. 'hot air balloon',
2. 'river',
3. 'terraced fields'.

```json
{
  "hot air balloon": [[74,35,117,84], [200,29,236,66], [411,43,442,69]],
  "river": [[223,285,400,406]],
  "terraced fields": [[0,228,600,477]]
}
```
    """
    coord_dict = extract_coord_keyword(content)
    print(coord_dict)
    assert coord_dict

    response = concat_content_coord(content, coord_dict)
    print(response)




@pytest.mark.asyncio
async def test_can_generate_content_and_coord_value_with_valid(img_data):
    # given : 유효한 데이터(이미지)
    # when : 생성 요청
    content = FocusPointManager().generate_content_and_coord(img_data)
    # then : 정상 응답
    print(content)
    assert len(content) > 0

    # given : 정상 응답된 값
    # when : 값에서 해설 키워드/좌표 추출
    coord_dict = extract_coord_keyword(content)
    assert coord_dict

    # then : 키워드/좌표/키워드 해설 추출
    # TODO : 좌표가 정상 추출되는지 확인
    assert len(coord_dict) > 0

    # given : 좌표값이 있는 경우
    if coord_dict:
        #when : 좌표값과 content 내용을 합차기
        response = concat_content_coord(content, coord_dict)
    # then : 출력값 응답
    print(response)
    assert response
