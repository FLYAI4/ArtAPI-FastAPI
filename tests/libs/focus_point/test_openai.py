import os
import pytest
import base64
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
async def test_cannot_refine_content_wrong_content():
    # given : 잘못된 데이터(좌표 값이 없는)
    wrong_content = """
Unfortunately, without the name or context of a particular artist, I am unable to provide a factual biography or discuss their personal achievements. However, I can still discuss the image provided in terms of its visual elements and style.

This painting is done in a highly stylized manner, with vibrant colors and exaggerated features that are reminiscent of Naïve or Folk Art styles. The bright, solid colors and the flattened perspective create a sense of whimsy and simplicity. There's a clear influence of pastoral and landscape traditions, yet with a modern twist in the way the natural elements are depicted with a surreal quality.

The image depicts a lush, rolling landscape with terraced fields, perhaps tea fields or rice paddies, which suggests an East Asian setting. There are trees distributed in a way that complements the curves of the land. In the distance, a winding river leads towards a calm, blue lake, surrounded by layered hills or mountains, emphasizing the depth of the scene. Hot air balloons float gently in the sky, adding a playful and fantastic element to the scene. A small red brick structure on the left adds a hint of human presence without overtaking the natural beauty of the scene.

Considering the elements in this image, here are three keywords with their respective coordinates:
"""
    # when : 파싱 요청
    refined_content = FocusPointManager().refine_content(wrong_content)
    # then : 빈 딕셔너리 응답
    assert not refined_content
    
    
@pytest.mark.asyncio
async def test_cannot_refine_content_wrong_json_format():
    # given : 잘못된 데이터(json 값을 잘 못 주는 경우)
    wrong_content = """
Unfortunately, without the name or context of a particular artist, I am unable to provide a factual biography or discuss their personal achievements. However, I can still discuss the image provided in terms of its visual elements and style.

This painting is done in a highly stylized manner, with vibrant colors and exaggerated features that are reminiscent of Naïve or Folk Art styles. The bright, solid colors and the flattened perspective create a sense of whimsy and simplicity. There's a clear influence of pastoral and landscape traditions, yet with a modern twist in the way the natural elements are depicted with a surreal quality.

The image depicts a lush, rolling landscape with terraced fields, perhaps tea fields or rice paddies, which suggests an East Asian setting. There are trees distributed in a way that complements the curves of the land. In the distance, a winding river leads towards a calm, blue lake, surrounded by layered hills or mountains, emphasizing the depth of the scene. Hot air balloons float gently in the sky, adding a playful and fantastic element to the scene. A small red brick structure on the left adds a hint of human presence without overtaking the natural beauty of the scene.

Considering the elements in this image, here are three keywords with their respective coordinates:
    ```json
    {
      'pearl_earring': [[233, 458, 278, 504], [1,1,1,1]],
      'blue_headscarf': [[120, 87, 360, 210]],
      'young_woman': [[76, 20, 478, 720]]
    }
    ```
"""
    # when : 파싱 요청
    refined_content = FocusPointManager().refine_content(wrong_content)
    # then : 빈 딕셔너리 응답
    assert not refined_content


@pytest.mark.asyncio
async def test_can_refine_content():
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
      "pearl_earring": [[233, 458, 278, 504], [1,1,1,1]],
      "blue_headscarf": [[120, 87, 360, 210]],
      "young_woman": [[76, 20, 478, 720]]
    }
    ```
```
    """
    refined_content = FocusPointManager().refine_content(content)
    assert refined_content


@pytest.mark.asyncio
async def test_cannot_refine_content_with_white_image():
    # given : 특징이 없는 흰색 이미지
    WHITE_IMG_PATH = os.path.abspath(os.path.join(test_img_path, "white.png"))
    with open(WHITE_IMG_PATH, "rb") as f:
        wrong_image = base64.b64encode(f.read()).decode('utf-8')
    # when : 파싱 요청
    refined_content = FocusPointManager().generate_content_and_coord(wrong_image)
    # then : 빈 딕셔너리 응답
    assert not refined_content


@pytest.mark.asyncio
async def test_can_generate_content_and_coord_value_with_valid(img_data):
    # given : 유효한 데이터(이미지)
    # when : 생성 요청
    refined_content = FocusPointManager().generate_content_and_coord(img_data)
    # then : 정상 응답
    assert len(refined_content) > 0
