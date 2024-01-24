import os
from datetime import datetime
from fastapi import UploadFile

def create_folder_if_not_exists(folder_path: str) -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return "Success create folder."
    return "Already exist folder."


def make_unique_name(username: str, extension=".png") -> str:
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d_%H%M%S")

    return f"{timestamp}_{username}{extension}"


async def save_image_local(image_file: UploadFile, file_name: str) -> str:
    libs_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
    imgs_path = os.path.abspath(os.path.join(libs_path, "img"))
    create_folder_if_not_exists(imgs_path)

    user_file_path = os.path.abspath(os.path.join(imgs_path, file_name))

    with open(user_file_path, "wb") as f:
        f.write(image_file.file.read())

    return user_file_path


async def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return "Success delete file."
    return "There is no file."
