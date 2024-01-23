from bson.binary import Binary
from fastapi import UploadFile
from .repository import Repository
from src.libs.util import (
    save_image_local,
    make_unique_name,
    delete_file
    )


class Service:
    def __init__(self, session) -> None:
        self.repo = Repository(session)

    def insert_image(self, username: str, image_file: UploadFile) -> str:
        file_name = make_unique_name(username, extension=".png")

        # img 파일의 재사용성을 고려해 로컬에 이미지 저장
        user_file_path = save_image_local(image_file, file_name)

        with open(user_file_path, "rb") as f:
            image_banary = Binary(f.read())

        data = {
            "_id": file_name,
            "username": username,
            "image": image_banary
            }
        self.repo.insert_image("tests", data)

        # 저장 완료 후 로컬 이미지 삭제
        delete_file(user_file_path)

        # TODO : 응답 수정
        return {
            "username": username
        }
