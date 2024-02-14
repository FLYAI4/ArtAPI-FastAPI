from pymongo import MongoClient
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, UploadFile, File, Header
from src.libs.db_manager import MongoManager, PostgreManager
from src.apps.user.service import UserService
from src.libs.api.validator import ApiValidator
from src.libs.api.util import make_response
from fastapi.responses import StreamingResponse
from src.apps.user.schema import UserImagePayload

user = APIRouter(prefix="/user")

@user.post('/image')
async def insert_image(
    id: str = Header(),
    token: str = Header(),
    file: UploadFile = File(...),
):
    ApiValidator.check_valid_token(id, token)
    result = UserService.insert_image(id, file)
    return make_response(result)


@user.post('/content')
async def make_generated_content(
    payload: UserImagePayload,
    id: str = Header(),
    token: str = Header(),
    postgre_session: Session = Depends(PostgreManager().get_session),
    mongo_session: MongoClient = Depends(MongoManager().get_session),
):
    ApiValidator.check_valid_token(id, token)
    return StreamingResponse(UserService.generate_content_with_image(
        postgre_session,
        mongo_session,
        id,
        payload.generated_id),
        media_type="text/event-stream")


@user.post('/video')
async def get_video_content(
    payload: UserImagePayload,
    id: str = Header(),
    token: str = Header(),
):
    ApiValidator.check_valid_token(id, token)
    video_contents = UserService.get_video(payload.generated_id)
    return StreamingResponse(video_contents, media_type="video/mp4")


@user.post('/content/demo')
async def make_generated_content_demo(
    payload: UserImagePayload,
    id: str = Header(),
    token: str = Header(),
):
    return StreamingResponse(UserService.generate_content_with_image_demo(payload.generated_id),
                             media_type="text/event-stream")


@user.post('/video/demo')
async def get_video_content_demo(
    payload: UserImagePayload,
    id: str = Header(),
    token: str = Header(),
):
    video_contents = UserService.get_video_demo(payload.generated_id)
    return StreamingResponse(video_contents, media_type="video/mp4")
