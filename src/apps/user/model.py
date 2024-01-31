import pydantic
from typing import Any


class UserGeneratedInfo(pydantic.BaseModel):
    origin_img: Any
