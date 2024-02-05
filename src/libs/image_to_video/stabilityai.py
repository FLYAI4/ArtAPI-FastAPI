import os
import requests
import time
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
        response = self.post_generated_video(resize_image_path)
        generated_id = response.json()["id"]
        origin_video_path = self.get_generated_video(generated_id, "origin_video.mp4")

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

    def get_generated_video(self, generated_id: str, origin_video_name: str):
        origin_video_path = os.path.abspath(os.path.join(self.user_folder_path, origin_video_name))

        flag = 0
        while flag != 200:
            response = requests.get(
                f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generated_id}",
                headers={
                    'Accept': None, # Use 'application/json' to receive base64 encoded JSON
                    'authorization': self.token
                },
            )

            # flag에 status code 할당
            flag = response.status_code
            if flag == 202:
                print("Generation in-progress... automatically try again after 3 sec.")
                time.sleep(3)
            elif flag == 200:
                print("Generation complete")
                with open(origin_video_path, 'wb') as file:
                    file.write(response.content)
                print(f"video Saved at {origin_video_path}")
            else:
                raise Exception("Non-200 response : " + str(response.json()))
        return origin_video_path
