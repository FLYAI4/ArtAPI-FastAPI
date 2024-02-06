import base64
import os
import io
from pymongo import MongoClient
from bson.binary import Binary
from fastapi import UploadFile
from src.apps.user.repository import UserRepository
from src.apps.user.model import UserGeneratedInfo
from src.libs.image_to_video.stabilityai import VideoManager
from src.libs.focus_point.openai import FocusPointManager
from src.libs.api.util import (
    generate_unique_id,
    save_file_local,
    find_storage_path
    )


class UserService:
    def insert_image(id: str, img_file: UploadFile):
        user_unique_id = generate_unique_id(id)
        save_file_local(img_file, user_unique_id, "origin_img.jpg")
        return {"generated_id": user_unique_id}

    async def generate_content_with_image(
        session: MongoClient,
        user_unique_id: str
    ):
        # Load images from local server
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(storage_path, user_unique_id))
        user_file_path = os.path.abspath(os.path.join(user_path, "origin_img.jpg"))
        with open(user_file_path, "rb") as f:
            base64_img = base64.b64encode(f.read()).decode('utf-8')
            origin_img = Binary(f.read())

        # Generate content and coordinate value
        content_generator = FocusPointManager().generate_content_and_coord(base64_img)
        text_content = await content_generator.__anext__()
        yield f"content: {text_content}\n".encode()
        coord_content = await content_generator.__anext__()
        yield f"coord: {str(coord_content)}\n".encode()

        # TODO: Demo 끝나면 저장하도록 수정 + PostgreSQL
        # Save user_data to MongoDB user_genreated document
        # user_data = UserGeneratedInfo(origin_img=origin_img).model_dump()
        # user_data["_id"] = user_unique_id
        # UserRepository.insert_image(session, user_data)
        yield "stream finished"

        await VideoManager(user_path).generate_video_content()
        
    def get_video(user_unique_id: str):
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(storage_path, user_unique_id))
        user_file_path = os.path.abspath(os.path.join(user_path, "slow_video.mp4"))
        
        with open(user_file_path, mode="rb") as video_file:
            # Read the contents of the video file
            video_contents = video_file.read()
            return io.BytesIO(video_contents)
