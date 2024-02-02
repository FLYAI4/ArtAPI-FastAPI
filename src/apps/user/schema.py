import pydantic


class UserImagePayload(pydantic.BaseModel):
    generated_id: str
