import os
import re
import json
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

    async def generate_content_and_coord(self, img_data: str = None):
        try:
            ori_content = await self.generate_content(img_data)
            ori_content = ori_content.replace('\n', ' ').replace('\t', '')
            # Get main content
            main_content = self.get_main_content(ori_content)
            if not main_content:
                raise FocusPointError(**FocusPointErrorCode.APIError.value)
            yield main_content

            # Get coord content
            if main_content:
                coord_content = self.get_coord_content(ori_content, main_content)
                # 좌표를 못찾을 경우 한 번더 실행
                if not coord_content:
                    content = self.generate_content(img_data)
                    coord_content = self.get_coord_content(content)
                yield coord_content
        except Exception as e:
            raise FocusPointError(**FocusPointErrorCode.APIError.value, err=e)

    async def generate_content(self, img_data: str):
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

    def get_coord_content(self, ori_content: str, main_content: str):
        coord_dict = self.__extract_coord_keyword(ori_content)
        if coord_dict:
            return self.__concat_content_coord(main_content, coord_dict)
        return {}

    @staticmethod
    def get_main_content(content):
        keyword = ':'
        if keyword in content:
            content = content[:content.find(keyword)].strip()

        main_content = ""
        words = ["cannot", "AI", "do not", "can't", "json", "JSON", "{", "Unfortunately", "coordinates", "However"]
        for sentence in list(content.split(".")):
            if not any(word in sentence for word in words):
                main_content += sentence + "."
        return main_content

    @staticmethod
    def __extract_coord_keyword(content: str):
        pattern = r'```json(.*?)```'
        json_data = re.search(pattern, content, re.DOTALL)
        try:
            data_dict = {}
            if json_data:
                json_string = json_data.group(1).strip()
                json_string = re.sub(r"\s", "", json_string)
                # issue : json.loads 할 때, 문자열 키와 문자열 값은 반드시 큰따옴표(double quotes)로 둘러싸야 함.
                data_dict = json.loads(json_string)
            return data_dict
        except Exception:
            return {}

    @staticmethod
    def __concat_content_coord(main_content: str, coord_dict: dict):
        # 설명 정제
        # keyword = ':'
        # if keyword in main_content:
        #     re_fined_content = main_content[:main_content.find(keyword)].strip()
        # # re_fined_content = content.replace("\n", " ").strip()

        response = {}
        for key, item in coord_dict.items():
            response[key] = {"coord": item, "context": ""}

        for sentence in list(main_content.split('. ')):
            for key in coord_dict.keys():
                if key.replace("_", " ") in sentence:
                    response[key]["context"] += sentence + ". "
                # context를 못찾는 경우 컨텍스트를 분리해서 한 번 더 탐색
                if not response[key]["context"]:
                    for separte_key in reversed(list(key.split("_"))):
                        if separte_key in sentence:
                            response[key]["context"] += sentence + ". "
                            break

        return response

    @staticmethod
    def __make_promt():
        promt_text = [
            "You are an expert art historian with vast knowledge about artists throughout history who revolutionized their craft.",
            "You will begin by briefly summarizing the personal life and achievements of the artist.",
            "Then you will go on to explain the medium, style, and influences of their works.",
            "Then you will provide short descriptions of what they depict and any notable characteristics they might have.",
            "Fianlly identify THREE keywords in the picture and provide each coordinate of the keywords in the last sentence.",
            'For example, Give the coordinate value of the keywords in json format such as if the keyword is Pretty_woman, ```json{"pretty_woman", [[x0,y0,x1,y1]]}```, or if there are multiple coordinates, keyword coordinates in json format such as ```json{"pretty_woman":[[x0,y0,x1,y1], [x2,y2,x3,y3]]}`',
            "The values ​​entered in x0, y0, x1, y1 are unconditionally the coordinate values ​​of each keyword."
        ]
        return " ".join(promt_text)
