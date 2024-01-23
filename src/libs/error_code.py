from enum import Enum


class DBErrorCode(Enum):
    DBConnectionError = {
        "code": 500,
        "message": "Failed to connect Mongodb. Contact service administrator.",
        "log": "DB Connect Error. Check DB module."
        }
    DBProcessError = {
        "code": 500,
        "message": "Failed to insert data. Contact service administrator.",
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
