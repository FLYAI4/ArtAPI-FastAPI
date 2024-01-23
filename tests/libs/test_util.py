import os
import pytest
from src.libs.util import create_folder_if_not_exists, delete_file

# Mock
libs_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_path = os.path.abspath(os.path.join(libs_path, "test"))
file_path = os.path.abspath(os.path.join(test_path, "test.txt"))


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_create_folder_and_file():
    # given : 유효한 경로(현재 경로에 새로운 폴더 생성)
    # when : 폴더 생성
    result = create_folder_if_not_exists(test_path)

    # then : Success create folder. 반환
    assert result == "Success create folder."

    # given : 이미 생성된 경로
    # when : 폴더 생성
    result = create_folder_if_not_exists(test_path)

    # then : Already exist folder. 반환
    assert result == "Already exist folder."

    # 파일 생성
    with open(file_path, "a") as f:
        f.write("hello\n")


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_delete_file():
    # given : 유효한 경로(test 폴더 안에 유효한 파일 존재)
    # when : 파일 삭제
    result = delete_file(file_path)

    # then : Success delete file. 반환
    assert result == "Success delete file."

    # given : 이미 삭제된 파일
    # when : 파일 삭제
    result = delete_file(file_path)

    # then : There is no file. 반환
    assert result == "There is no file."

    if os.path.exists(test_path):
        os.removedirs(test_path)
