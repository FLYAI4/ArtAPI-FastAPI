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
    NonHeaderError = {
        "code": 401,
        "message": "There is non header. Please log in again.",
        "log": "User request fail with non header."
    }
    NonFileError = {
        "code": 401,
        "message": "There is non file. Please request again.",
        "log": "User request fail with non file."
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
