import pydantic


class UserSignupPayload(pydantic.BaseModel):
    email: str
    password: str
    name: str
    gender: str
    age: str


class UserLoginPayload(pydantic.BaseModel):
    email: str
    password: str
