import base64
import os
import io
from pymongo import MongoClient
from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.apps.user.repository import UserRepository
from src.apps.user.model import UserGeneratedInfo
from src.libs.image_to_video.stabilityai import VideoManager
from src.libs.focus_point.openai import FocusPointManager
from src.libs.api.util import (
    generate_unique_id,
    save_file_local,
    find_storage_path
    )
from PIL import Image


class UserService:
    def insert_image(id: str, img_file: UploadFile):
        user_unique_id = generate_unique_id(id)
        save_file_local(img_file, user_unique_id, "origin_img.jpg")
        return {"generated_id": user_unique_id}

    async def generate_content_with_image(
        postgre_session: Session,
        mongo_session: MongoClient,
        id: str,
        user_unique_id: str
    ):
        # Load images from local server
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(storage_path, user_unique_id))
        user_file_path = os.path.abspath(os.path.join(user_path, "origin_img.jpg"))


        # with open(user_file_path, "rb") as f:
        #     base64_img = base64.b64encode(f.read()).decode('utf-8')
        #     # origin_img = Binary(f.read())

        # image compress
        img = Image.open(user_file_path)
        output = io.BytesIO()
        img.convert("RGB").save(output, format='JPEG', quality=50)
        output.seek(0)
        base64_img = base64.b64encode(output.read()).decode('utf-8')

        # Generate content and coordinate value
        content_generator = FocusPointManager().generate_content_and_coord(base64_img)
        text_content = await content_generator.__anext__()
        yield f"content: {text_content}\n".encode()
        coord_content = await content_generator.__anext__()
        yield f"coord: {str(coord_content)}\n".encode()

        # Save user_data to MongoDB user_genreated document
        user_data = UserGeneratedInfo(origin_img=base64_img,
                                      text_content=str(text_content),
                                      coord_content=str(coord_content)).model_dump()
        user_data["_id"] = user_unique_id
        UserRepository.insert_image(mongo_session, user_data)
        yield "stream finished"

        UserRepository.insert_generated_id(postgre_session, id, user_unique_id)

        await VideoManager(user_path).generate_video_content()
        
    def get_video(user_unique_id: str):
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(storage_path, user_unique_id))
        user_file_path = os.path.abspath(os.path.join(user_path, "slow_video.mp4"))
        
        with open(user_file_path, mode="rb") as video_file:
            # Read the contents of the video file
            video_contents = video_file.read()
            return io.BytesIO(video_contents)

    async def generate_content_with_image_demo(user_unique_id: str):
        text_content = "Vincent van Gogh was a Dutch post-impressionist painter who is among the most famous and influential figures in the history of Western art. He was born on March 30, 1853, and passed away on July 29, 1890. Despite that, his fame grew posthumously, and his works became celebrated for their emotional honesty, bold color, and innovative application of paint.  Van Gogh worked with a variety of media, including oil on canvas, and he is known for his expressive and emotive use of vibrant color and energetic application of impastoed paint. His style, while grounded in impressionism, moved toward what would become known as expressionism.  His influences ranged widely, from the realism of Millet to the impressionistic light and color of the Paris art scene. Japanese prints also influenced his work, which can be seen in his use of color and compositions.  \"The Starry Night,\" one of Van Gogh's most famous works, depicts a swirling night sky filled with yellow, glowing stars over a small village. It features a prominent cypress tree in the foreground, which could symbolize death, eternal life, or both, as cypresses are often found in cemeteries and yet are also evergreen. The swirling patterns of the sky create a dynamic movement, conveying deep emotional resonance, where the night sky becomes a field of roiling energy."
        yield f"content: {text_content}\n".encode()
        coord_content = "{'starry_sky': {'coord': [[0, 0, 600, 250]], 'context': ' \"The Starry Night,\" one of Van Gogh\'s most famous works, depicts a swirling night sky filled with yellow, glowing stars over a small village. '}, 'cypress_tree': {'coord': [[200, 290, 250, 475]], 'context': 'It features a prominent cypress tree in the foreground, which could symbolize death, eternal life, or both, as cypresses are often found in cemeteries and yet are also evergreen. '}, 'village': {'coord': [[10, 370, 400, 475]], 'context': ' \"The Starry Night,\" one of Van Gogh\'s most famous works, depicts a swirling night sky filled with yellow, glowing stars over a small village. '}}"
        yield f"coord: {str(coord_content)}\n".encode()

        yield "stream finished"

    def get_video_demo(user_unique_id: str):
        user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
        demo_path = os.path.abspath(os.path.join(user_path, "demo"))
        user_file_path = os.path.abspath(os.path.join(demo_path, "slow_video.mp4"))

        with open(user_file_path, mode="rb") as video_file:
            # Read the contents of the video file
            video_contents = video_file.read()
            return io.BytesIO(video_contents)
