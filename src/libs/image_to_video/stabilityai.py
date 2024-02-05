import os
import requests
from PIL import Image


class VideoManager:
    def __init__(self, user_folder_path: str,
                 token: str = os.environ.get("STABILITY_AI_TOKEN_KEY", 'utf-8')
                 ) -> None:
        self.width = 768
        self.height = 768
        self.user_folder_path = user_folder_path
        self.token = token
        self.seed = 0
        self.cfg_scale = 2.5
        self.motion_bucket_id = 40

    def generate_video_content(self):
        resize_image_path = self.resize_image("origin_img.jpg")
        self.post_generated_video(resize_image_path)

    def resize_image(self, origin_img_name: str):
        # base image
        origin_img_path = os.path.abspath(os.path.join(self.user_folder_path, origin_img_name))
        image = Image.open(origin_img_path)

        # resize
        resized_image_path = os.path.abspath(os.path.join(self.user_folder_path, "resized_img.jpg"))
        resized_image = image.resize((self.width, self.height))
        resized_image.save(resized_image_path)

        return resized_image_path

    def post_generated_video(self, resized_img_name: str):
        # resized_image_path
        resize_image_path = os.path.abspath(os.path.join(self.user_folder_path, resized_img_name))
        
        # request generated video to stability ai
        response = requests.post(
            "https://api.stability.ai/v2alpha/generation/image-to-video",
            headers={
                "authorization": "Bearer " + self.token,
            },
            data={
                "seed": self.seed,
                "cfg_scale": self.cfg_scale,
                "motion_bucket_id": self.motion_bucket_id
            },
            files={
                "image": ("file", open(resize_image_path, "rb"), "image/png")
            },
        )
        # TODO : 예외 처리 필요
        return response
