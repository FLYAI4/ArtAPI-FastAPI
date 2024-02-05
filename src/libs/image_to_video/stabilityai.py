import os
from PIL import Image


class VideoManager:
    def __init__(self, user_folder_path: str) -> None:
        self.width = 768
        self.height = 768
        self.user_folder_path = user_folder_path

    def generate_video_content(self):
        resize_image_path = self.resize_image(self.user_folder_path)

    def resize_image(self):
        # base image
        origin_img_path = os.path.abspath(os.path.join(self.user_folder_path, "origin_img.jpg"))
        image = Image.open(origin_img_path)

        # resize
        resize_image_path = os.path.abspath(os.path.join(self.user_folder_path, "resized_img.jpg"))
        resize_image = image.resize((self.width, self.height))
        resize_image.save(resize_image_path)

        return resize_image_path
