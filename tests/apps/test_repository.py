import pytest


@pytest.mark.asyncio
async def test_user_repository_can_insert_data_with_valid():
    # given : 유요한 데이터(사용자 정보 + 이미지 정보)

    # when : DB에 데이터 저장

    # then : 사용자 정보 + 이미지 경로 반환
    pass


@pytest.mark.asyncio
async def test_user_repository_cannot_insert_data_with_infalid():
    # give : 유요한 데이터(사용자 정보 + 이미지 정보)

    # when : DB에 데이터 저장 시 DB연결 오류

    # then : 에러메시지 반환
    pass
