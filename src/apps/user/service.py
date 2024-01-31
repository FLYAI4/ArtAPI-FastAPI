from bson.binary import Binary
from fastapi import UploadFile
from src.apps.user.repository import UserRepository
from src.apps.user.model import UserGeneratedInfo
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
        # Save image to local server
        user_unique_id = generate_unique_id(id)
        user_file_path = await save_file_local(image_file, user_unique_id, "origin_img")

        # Load images from local server
        with open(user_file_path, "rb") as f:
            origin_img = Binary(f.read())
        user_data = UserGeneratedInfo(origin_img=origin_img).model_dump()

        # Save user_data to MongoDB user_genreated document
        user_data["_id"] = user_unique_id
        UserRepository.insert_image(session, user_data)

        # Delete local server image after saving is complete
        # TODO : 1시간 뒤에 폴더 기준으로 삭제하도록 수정
        await delete_file(user_file_path)

        return {
            "id": id
        }
