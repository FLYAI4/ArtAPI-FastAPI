from fastapi import APIRouter, Depends, UploadFile, File, Header
from src.libs.db_manager import MongoManager
from src.libs.exception import UserError
from src.libs.error_code import UserRequestErrorCode
from src.apps.service import Service

user = APIRouter(prefix="/user")


@user.post('/content')
async def make_generated_content(
    username: str = Header(default=None),
    file: UploadFile = File(default=None)
):
    # TODO : mongodb 의존성 추가
    session = MongoManager().get_session()
    if not username:
        raise UserError(**UserRequestErrorCode.NonHeaderError.value)
    if not file:
        raise UserError(**UserRequestErrorCode.NonFileError.value)

    result = await Service(session).insert_image(username, file)
    return {
        "meta": {
            "code": 200,
            "message": "ok"
        },
        "data": result
    }
