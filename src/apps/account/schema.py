import pydantic


class UserSignupPayload(pydantic.BaseModel):
    id: str
    password: str
    name: str
    gender: str
    age: str


class UserLoginPayload(pydantic.BaseModel):
    id: str
    password: str
