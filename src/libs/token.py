import os
import jwt
from datetime import datetime, timedelta


class TokenManager:
    def __init__(self) -> None:
        self.TOKEN_KEY = os.environ.get('TOKEN_KEY')

    def create_token(self, user_id: str):
        return jwt.encode({
                "email": user_id,
                "exp": datetime.utcnow() + timedelta(hours=5)
            }, self.TOKEN_KEY, algorithm="HS256")

    def decode_token(self, token: str):
        return jwt.decode(token, self.TOKEN_KEY, algorithms="HS256")
