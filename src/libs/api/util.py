import os
from datetime import datetime
from fastapi import UploadFile


def create_folder_if_not_exists(folder_path: str) -> str:
    """Create folder if not exists."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return "Success create folder."
    return "Already exist folder."


def generate_unique_id(user_id: str) -> str:
    """Generate unique id according to API request."""
    id = user_id.split("@")[0]
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{id}"


async def save_file_local(file: UploadFile, user_unique_id: str, file_name: str) -> str:
    """Save file to local storage folder"""
    # Set file path
    api_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
    libs_path = os.path.abspath(os.path.join(api_path, os.path.pardir))
    src_path = os.path.abspath(os.path.join(libs_path, os.path.pardir))
    root_path = os.path.abspath(os.path.join(src_path, os.path.pardir))
    storage_path = os.path.abspath(os.path.join(root_path, 'storage'))
    create_folder_if_not_exists(storage_path)

    # Create folders for each user
    user_path = os.path.abspath(os.path.join(storage_path, user_unique_id))
    create_folder_if_not_exists(user_path)

    # Save file
    file_extension = file.filename.split(".")[-1]
    full_file_name = file_name + "." + file_extension
    user_file_path = os.path.abspath(os.path.join(user_path, full_file_name))
    with open(user_file_path, "wb") as f:
        f.write(file.file.read())
    return user_file_path


async def delete_file(file_path):
    """Delete file if exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
        return "Success delete file."
    return "There is no file."


def make_response(resp: any):
    """Make response to send response."""
    return {
        "meta": {
            "code": 200,
            "message": "ok"
        },
        "data": resp
    }
