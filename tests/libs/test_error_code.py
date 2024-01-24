import pytest
from src.libs.error_code import DBErrorCode


@pytest.mark.asyncio
async def test_DBErrorCode_enum_class():
    assert DBErrorCode.DBProcessError.value == {
        "code": 500,
        "message": "Failed to insert data. Contact service administrator.",
        "log": "DB Process Error. Check DB module."
    }
