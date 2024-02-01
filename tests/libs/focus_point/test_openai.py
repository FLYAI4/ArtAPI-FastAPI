import pytest


@pytest.mark.asyncio
async def test_cannot_content_and_coord_value_with_on_token():
    # given : 유효한 데이터(이미지) + 계정에 토큰이 없는 경우

    # when : 생성 요청

    # then : 비정상 응답
    pass


@pytest.mark.asyncio
async def test_cannot_content_and_coord_value_with_no_image():
    # given : 빈 데이터

    # when : 생성 요청

    # then : 비정상 응답
    pass


@pytest.mark.asyncio
async def test_can_generate_content_and_coord_value_with_valid():
    # given : 유효한 데이터(이미지)

    # when : 생성 요청

    # then : 정상 응답

    # given : 정상 응답된 값

    # when : 값에서 해설 키워드/좌표 추출

    # then : 키워드/좌표/키워드 해설 추출
    pass
