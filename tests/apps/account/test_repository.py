import pytest


@pytest.mark.asyncio
async def test_account_repository_cannot_insert_user_account():
    # given : DB에 테이블이 생성되지 않을 때(DB 연결 오류)

    # when : DB 데이터 입력 요청

    # then : DB 연결 오류 메시지
    pass

@pytest.mark.asyncio
async def test_account_repository_cannot_get_all_user_account():
    # given : 테이블에 아무 데이터도 없을 때

    # when : DB 데이터 조회 요청

    # then : 빈 리스트 출력
    pass


@pytest.mark.asyncio
async def test_account_repository_can_insert_user_account():
    # given : 유효한 유저 정보

    # when : DB에 데이터 입력 요청

    # then : 데이터 입력 확인(id)
    pass


@pytest.mark.asyncio
async def test_account_repository_can_update_user_account():
    # given : 변경할 유저 정보(ID제외)

    # when : DB에 데이터 변경 요청

    # then : 변경된 데이터 확인
    pass


@pytest.mark.asyncio
async def test_account_repository_can_get_user_account():
    # given : 조회할 유저 ID

    # when : DB에 데이터 조회 요청

    # then : 조회된 데이터 확인
    pass

@pytest.mark.asyncio
async def test_account_respository_can_get_all_user_account():
    # given :

    # when : DB에 데이터 전체 조회 요청

    # then : 조회된 데이터 확인
    pass
