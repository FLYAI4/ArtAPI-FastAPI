import os
import requests
from src.libs.api.exception import FocusPointError
from src.libs.api.error_code import FocusPointErrorCode


class FocusPointManager:
    def __init__(self, token: str = os.environ.get("OEPN_AI_TOKEN_KEY",
                                                   'utf-8')) -> None:
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }

    def generate_content_and_coord(self, img_data: str = None):
        return self.generate_content(img_data)

    def generate_content(self, img_data: str):
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.__make_promt(),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 800
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=self.headers,
                                 json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]["message"]["content"]
        elif response.status_code == 400:
            raise FocusPointError(**FocusPointErrorCode.NonImageError.value,
                                  err=response.json()["error"])
        elif response.status_code == 404:
            raise FocusPointError(**FocusPointErrorCode.NonTokenError.value,
                                  err=response.json()["error"])
        else:
            raise FocusPointError(**FocusPointErrorCode.UnknownError.value,
                                  err=response.json()["error"])

    @staticmethod
    def __make_promt():
        new_promt_text = [
            "You are an expert art historian with vast knowledge about artists throughout history who revolutionized their craft.",
            "You will begin by briefly summarizing the personal life and achievements of the artist.",
            " hen you will go on to explain the medium, style, and influences of their works.",
            "Then you will provide short descriptions of what they depict and any notable characteristics they might have.",
            "Fianlly identify THREE keywords in the picture and provide each coordinate of the keywords in the last sentence.",
            "For example if the keyword is woman, the output must be 'woman':[[x0,y0,x1,y1]] or 'woman':[[x0,y0,x1,y1], [x2,y2,x3,y3]].",
            "Give the keyword value in json format like {'woman', [[x0,y0,x1,y1]]} or {'woman':[[x0,y0,x1,y1], [x2,y2,x3,y3]]}."
        ]
        return " ".join(new_promt_text)
