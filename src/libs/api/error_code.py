from enum import Enum


class DBErrorCode(Enum):
    DBConnectionError = {
        "code": 500,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Connect Error. Check DB module."
        }
    DBProcessError = {
        "code": 500,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Process Error. Check DB module."
    }


class SystemErrorCode(Enum):
    OSModuleError = {
        "code": 500,
        "message": "System error. Contact service administrator.",
        "log": "OSModule Error. Check os library"
    }


class UserRequestErrorCode(Enum):
    NonMatchEmail = {
        "code": 401,
        "message": "The ID is not in email format. Please enter again.",
        "log": "User service sign up fail with wrong email."
    }
    AlreadyUserError = {
        "code": 401,
        "message": "The user email is already created. Please sign up another email.",
        "log": "User service sign up fail with already existence email."
    }
    NonSignupError = {
        "code": 401,
        "message": "This account is not registered. Please sign up.",
        "log": "User request fail with non sign account."
    }
    WrongPasswordError = {
        "code": 401,
        "message": "The password is incorrect. Please check again..",
        "log": "User request fail with wrong password."
    }


class FocusPointErrorCode(Enum):
    NonImageError = {
        "code": 400,
        "message": "The ID is no image. Please image upload again.",
        "log": "Focus Point API request error with non image."
    }
    NonTokenError = {
        "code": 404,
        "message": "Failed to connect. Contact service administrator.",
        "log": "Focus Point API request error with non token. Please purchase token."
    }
    UnknownError = {
        "code": 500,
        "message": "Failed to connect. Contact service administrator.",
        "log": "Unkonw focus point error. Please check error log."
    }
    APIError = {
        "code": 500,
        "message": "Failed to request. Contact service administrator.",
        "log": "API Error. Please check api."
    }
