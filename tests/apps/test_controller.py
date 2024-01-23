import pytest

# TODO : 작품이 아닌 일반 사진을 넣었을 때 어떻게 처리할 것인지 고민!!


@pytest.mark.asyncio
async def test_user_can_make_generate_content():
    # given : 유효한 payload (header : username, file: UpladFile)

    # when : 콘텐츠 생성 API 요청

    # given : 정상 응답 username
    pass


@pytest.mark.asyncio
async def test_user_cannot_make_generate_content_with_non_header():
    # given : 유효하지 않은 payload (header 없이 요청)

    # when : 콘텐츠 생성 API 요청

    # given : 에러메시지
    pass


@pytest.mark.asyncio
async def test_user_cannot_make_generate_content_with_non_file():
    # given : 유효하지 않은 payload (file 없이 요청)

    # when : 콘텐츠 생성 API 요청

    # given : 에러메시지
    pass
