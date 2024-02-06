import os
import cv2
import requests
import time
from PIL import Image
from src.libs.api.exception import ImageToVideoError
from src.libs.api.error_code import ImageToVideoErrorCode

class VideoManager:
    def __init__(self, user_folder_path: str,
                 token: str = os.environ.get("STABILITY_AI_TOKEN_KEY", 'utf-8')
                 ) -> None:
        self.width = 768
        self.height = 768
        self.user_folder_path = user_folder_path
        self.token = token
        self.seed = 0
        self.cfg_scale = 2.5
        self.motion_bucket_id = 40

    def generate_video_content(self):
        # resize image to 768 * 768
        resize_image_path = self.resize_image("origin_img.jpg")
        
        # Request post video creation from stability ai
        response = self.post_generated_video(resize_image_path)
        generated_id = response.json()["id"]
        
        # Request get generated_video from stability ai
        origin_video_path = self.get_generated_video(generated_id, "origin_video.mp4")
        
        # Reverse playback to extend video length with openCV
        reversed_video_path = self.reverse_generated_video(origin_video_path, "reversed_video.mp4")
        
        # Play slowly to increase video length
        slow_video_path = self.slow_generated_video(reversed_video_path, "slow_video.mp4")
        return slow_video_path

    def resize_image(self, origin_img_name: str):
        """
        Resize image for stability AI request.
        Params:
            - origin_img_name: 원본 이미지 이름
        Return:
            - resized_image_path: 크기가 변경된 이미지 파일 경로
        Description:
            - supported image dim : (1024x576) (576x1024) (768x768)
        """
        # origin image
        origin_img_path = os.path.abspath(os.path.join(self.user_folder_path, origin_img_name))
        image = Image.open(origin_img_path)

        # resize
        resized_image_path = os.path.abspath(os.path.join(self.user_folder_path, "resized_img.jpg"))
        resized_image = image.resize((self.width, self.height))
        resized_image.save(resized_image_path)

        return resized_image_path

    def post_generated_video(self, resized_img_name: str):
        """
        Post generated video from stability ai
        Params:
            - resized_img_name: 사이즈 변경된 이미지 이름
        Return:
            - response
        """
        resize_image_path = os.path.abspath(os.path.join(self.user_folder_path, resized_img_name))

        # request generated video to stability ai
        response = requests.post(
            "https://api.stability.ai/v2alpha/generation/image-to-video",
            headers={
                "authorization": "Bearer " + self.token,
            },
            data={
                "seed": self.seed,
                "cfg_scale": self.cfg_scale,
                "motion_bucket_id": self.motion_bucket_id
            },
            files={
                "image": ("file", open(resize_image_path, "rb"), "image/png")
            },
        )
        if response.status_code == 200:
            return response
        elif 400 <= response.status_code < 500:
            raise ImageToVideoError(**ImageToVideoErrorCode.NonTokenError.value, err=str(response.json()))
        else:
            raise ImageToVideoError(**ImageToVideoErrorCode.APIError.value, err=str(response.json()))

    def get_generated_video(self, generated_id: str, origin_video_name: str):
        """
        Get generated video from stability ai
        Params:
            - generated_id: 이미지의 아이디
            - origin_video_name: 저장할 비디오 이름
        Return:
            - origin_video_path: 저장한 비디오 경로
        """
        origin_video_path = os.path.abspath(os.path.join(self.user_folder_path, origin_video_name))

        flag = 0
        while flag != 200:
            response = requests.get(
                f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generated_id}",
                headers={
                    'Accept': None, # Use 'application/json' to receive base64 encoded JSON
                    'authorization': self.token
                },
            )

            # flag에 status code 할당
            flag = response.status_code
            if flag == 202:
                print("Generation in-progress... automatically try again after 3 sec.")
                time.sleep(3)
            elif flag == 200:
                print("Generation complete")
                with open(origin_video_path, 'wb') as file:
                    file.write(response.content)
                print(f"video Saved at {origin_video_path}")
            else:
                raise ImageToVideoError(**ImageToVideoErrorCode.APIError.value, err=str(response.json()))
        return origin_video_path

    def reverse_generated_video(
        self,
        origin_video_path: str,
        reverse_video_name: str
    ):
        """
        reverse generated video with openCV
        Params:
            - origin_video_path: 원본 생성 비디오 경로
            - reverse_video_name: 역방향 재생 비디오 이름
        Return:
            - reversed_video_path: 역방향 재생 비디오 경로
        """
        reversed_video_path = os.path.abspath(os.path.join(self.user_folder_path, reverse_video_name))
        video = self.__set_video_object(origin_video_path, reversed_video_path)
        video = self.__play_video(origin_video_path, video, reverse=False)
        self.__play_video(origin_video_path, video, reverse=True)

        return reversed_video_path

    def slow_generated_video(
        self,
        reversed_video_path: str,
        slow_video_name: str
    ):
        """
        slow generated video with openCV
        Params:
            - reversed_video_path: 역방항 재생 비디오 경로
            - slow_video_name: 느리게 재생 비디오 이름
        Return:
            - slow_video_path: 느리게 재생 비디오 경로
        """
        slow_video_path = os.path.abspath(os.path.join(self.user_folder_path, slow_video_name))
        video = self.__set_video_object(reversed_video_path, slow_video_path)
        self.__play_video(reversed_video_path, video, double=True)
        return slow_video_path

    def __play_video(
        self,
        video_path: str,
        output_video: cv2.VideoWriter,
        reverse: bool = False,
        double: bool = False
    ):
        # 비디오 캡쳐 객체 생성
        cap = cv2.VideoCapture(video_path)
        # 비디오 재생
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # 출력 비디오에 현재 프레임 쓰기
            frames.append(frame)
            if double:
                frames.append(frame)

        if reverse:
            frames = reversed(frames)

        for frame in frames:
            output_video.write(frame)

        # 비디오 역재생을 위해 비디오 캡쳐 객체 초기화
        cap.release()
        return output_video

    def __set_video_object(self, input_video_path: str, output_video_path: str):
        cap = cv2.VideoCapture(input_video_path)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fps = int(cap.get(5))

        return cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
