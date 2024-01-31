import os
import jwt
from datetime import datetime, timedelta


class TokenManager:
    def __init__(self) -> None:
        self.TOKEN_KEY = os.environ.get('TOKEN_KEY')

    def create_token(self, id: str):
        return jwt.encode({
                "id": id,
                "exp": datetime.utcnow() + timedelta(hours=5)
            }, self.TOKEN_KEY, algorithm="HS256")

    def decode_token(self, token: str):
        return jwt.decode(token, self.TOKEN_KEY, algorithms="HS256")
