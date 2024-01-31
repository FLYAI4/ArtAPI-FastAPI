from src.libs.api.error_code import DBErrorCode


def test_DBErrorCode_enum_class():
    assert DBErrorCode.DBProcessError.value == {
        "code": 500,
        "message": "Failed to connect. Contact service administrator.",
        "log": "DB Process Error. Check DB module."
    }
