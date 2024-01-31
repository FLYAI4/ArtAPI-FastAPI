from pymongo import MongoClient
from fastapi import APIRouter, Depends, UploadFile, File, Header
from src.libs.db_manager import MongoManager
from src.apps.user.service import UserService
from src.libs.api.util import make_response

user = APIRouter(prefix="/user")


@user.post('/content')
async def make_generated_content(
    id: str = Header(),
    file: UploadFile = File(),
    session: MongoClient = Depends(MongoManager().get_session)
):
    result = await UserService.insert_image(session, id, file)
    return make_response(result)
