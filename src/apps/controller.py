from pymongo import MongoClient
from fastapi import APIRouter, Depends, UploadFile, File, Header
from src.libs.db_manager import MongoManager
from src.libs.exception import UserError
from src.libs.error_code import UserRequestErrorCode
from src.apps.service import Service
from src.libs.util import make_response

user = APIRouter(prefix="/user")


@user.post('/content')
async def make_generated_content(
    username: str = Header(default=None),
    file: UploadFile = File(default=None),
    session: MongoClient = Depends(MongoManager().get_session)
):
    if not username:
        raise UserError(**UserRequestErrorCode.NonHeaderError.value)
    if not file:
        raise UserError(**UserRequestErrorCode.NonFileError.value)

    result = await Service.insert_image(session, username, file)
    return make_response(result)
