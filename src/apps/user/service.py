from bson.binary import Binary
from fastapi import UploadFile
from src.apps.user.repository import UserRepository
from src.libs.api.util import (
    generate_unique_id,
    save_file_local,
    delete_file
    )


class UserService:
    async def insert_image(
        session,
        id: str,
        image_file: UploadFile
    ) -> dict:

        # img 파일의 재사용성을 고려해 로컬에 이미지 저장
        user_unique_id = generate_unique_id(id)
        user_file_path = await save_file_local(image_file, user_unique_id, "origin_img")

        with open(user_file_path, "rb") as f:
            image_banary = Binary(f.read())

        data = {
            "_id": user_unique_id,
            "origin_img": image_banary
            }
        UserRepository.insert_image(session, "user_generated", data)

        # 저장 완료 후 로컬 이미지 삭제
        await delete_file(user_file_path)

        return {
            "id": id
        }
