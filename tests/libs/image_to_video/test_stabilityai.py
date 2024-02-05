import os
import time
import cv2
import pytest
import requests
from dotenv import load_dotenv
from PIL import Image
from src.libs.image_to_video.stabilityai import VideoManager

# Setting
load_dotenv()
focus_point_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_folder_path = os.path.abspath(os.path.join(focus_point_path, "test_img"))
NO_TOKEN_ID_KEY = os.environ.get("STABILITY_AI_NO_TOKEN_KEY", 'utf-8')
TOKEN_KEY = os.environ.get("STABILITY_AI_NO_TOKEN_KEY", 'utf-8')

# Mockup
IMG_PATH = os.path.abspath(os.path.join(test_img_folder_path, "origin_img.jpg"))
SEED = 0
CFG_SCALE = 2.5
MOTION_BUCKET_ID=40
GENERATE_ORIGIN_VIDEO_PATH = os.path.abspath(os.path.join(test_img_folder_path, "generate_origin_video.mp4"))
REVERSED_VIDEO_PATH = os.path.abspath(os.path.join(test_img_folder_path, "reversed_video.mp4"))
SLOW_VIDEO_PATH = os.path.abspath(os.path.join(test_img_folder_path, "slow_video.mp4"))


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_can_resize_image():
    # given : 유효한 이미지
    # when : 이미지 사이즈 변경 요청
    resize_image_path = VideoManager(test_img_folder_path).resize_image()

    # then : 이미지 저장 파일 확인
    assert os.path.exists(resize_image_path)


# @pytest.mark.order(2)
# @pytest.mark.asyncio
# async def test_can_request_generate_video():
#     # given : 유효한 토큰 + 이미지
#     RESIZED_IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "resized_img.jpg"))

#     # when : 비디오 생성 요청
#     response = requests.post(
#         "https://api.stability.ai/v2alpha/generation/image-to-video",
#         headers={
#             "authorization": "Bearer " + TOKEN_KEY,
#         },
#         data={
#             "seed": SEED,
#             "cfg_scale": CFG_SCALE,
#             "motion_bucket_id": MOTION_BUCKET_ID
#         },
#         files={
#             "image": ("file", open(RESIZED_IMAGE_PATH, "rb"), "image/png")
#         },
#     )

#     # then : 생성 요청 확인
#     print(response.json())
#     assert response.status_code == 200
#     assert len(response.json()["id"]) > 0


# def test_cannot_request_generate_video_with_non_token():
#     # given : 토큰 부족 + 이미지
#     IMG_PATH = os.path.abspath(os.path.join(test_img_path, "test.png"))

#     # when : 비디오 생성 요청
#     response = requests.post(
#         "https://api.stability.ai/v2alpha/generation/image-to-video",
#         headers={
#             "authorization": "Bearer "+ NO_TOKEN_ID_KEY,
#         },
#         data={
#             "seed": SEED,
#             "cfg_scale": CFG_SCALE,
#             "motion_bucket_id": MOTION_BUCKET_ID
#         },
#         files={
#             "image": ("file", open(IMG_PATH, "rb"), "image/png")
#         },
#     )

#     # then : 토큰 부족 메시지
#     print(response.json())
#     assert response.status_code == 404


# def test_cannnot_request_generate_video_with_non_image():
#     # given : 유효한 토큰 + 이미지 없음
#     no_image_path = os.path.abspath(os.path.join(test_img_path, "no_image.jpg"))

#     # when : 비디오 생성 요청
#     # then : 이미지 없음 메시지
#     with pytest.raises(FileNotFoundError):
#         response = requests.post(
#             "https://api.stability.ai/v2alpha/generation/image-to-video",
#             headers={
#                 "authorization": "Bearer " + TOKEN_KEY,
#             },
#             data={
#                 "seed": SEED,
#                 "cfg_scale": CFG_SCALE,
#                 "motion_bucket_id": MOTION_BUCKET_ID
#             },
#             files={
#                 "image": ("file", open(no_image_path, "rb"), "image/png")
#             },
#         )
#         assert response.status_code == 200

# # TODO : pytest.mark.order 추가!!
# def test_can_get_generated_video():
#     # given : 생성된 비디오 요청 id
#     # when : 비디오 전달 요청
#     flag = 0
#     while flag != 200:
#         response = requests.get(
#             f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{GENERATED_ID}",
#             headers={
#                 'Accept': None, # Use 'application/json' to receive base64 encoded JSON
#                 'authorization': TOKEN_KEY
#             },
#         )
        
#         # flag에 status code 할당
#         flag = response.status_code
#         if flag == 202:
#             print("Generation in-progress... automatically try again after 3 sec.")
#             time.sleep(3)
#         elif flag == 200:
#             print("Generation complete")
#             with open(GENERATE_ORIGIN_VIDEO_PATH, 'wb') as file:
#                 file.write(response.content)
#             print(f"video Saved at {GENERATE_ORIGIN_VIDEO_PATH}")
#         else:
#             raise Exception("Non-200 response : " + str(response.json()))

#     # then : 비디오 전달 확인
#     assert os.path.exists(GENERATE_ORIGIN_VIDEO_PATH)

# def reverse_generated_video(output_video: cv2.VideoWriter, reverse: bool = False):
#     # 비디오 캡쳐 객체 생성
#     cap = cv2.VideoCapture(GENERATE_ORIGIN_VIDEO_PATH)
#     # 비디오 재생
#     frames = []
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # 출력 비디오에 현재 프레임 쓰기
#         frames.append(frame)
#     if reverse:
#         frames = reversed(frames)

#     for frame in frames:
#         output_video.write(frame)

#     # 비디오 역재생을 위해 비디오 캡쳐 객체 초기화
#     cap.release()


# def test_can_reverse_generated_video():
#     # given : 유효한 비디오 파일
#     # when : 비디오 파일 역 재생 및 연결
#     # 비디오 속성 가져오기
#     cap = cv2.VideoCapture(GENERATE_ORIGIN_VIDEO_PATH)
#     frame_width = int(cap.get(3))
#     frame_height = int(cap.get(4))
#     fps = int(cap.get(5))

#     # 비디오 작성 객체 생성
#     out = cv2.VideoWriter(REVERSED_VIDEO_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
#     reverse_generated_video(out, reverse=False)
#     reverse_generated_video(out, reverse=True)

#     # then : 비디오 파일 유효성 확인
#     assert os.path.exists(REVERSED_VIDEO_PATH)


# def test_can_slow_generated_video():
#     # given : 유효한 비디오 파일

#     # when : 비디오 파일 느리게
#     # 비디오 캡쳐 객체 생성
#     cap = cv2.VideoCapture(REVERSED_VIDEO_PATH)

#     # 비디오 속성 가져오기
#     frame_width = int(cap.get(3))
#     frame_height = int(cap.get(4))
#     fps = int(cap.get(5))

#     # 비디오 작성 객체 생성
#     slow_video = cv2.VideoWriter(SLOW_VIDEO_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

#     # 비디오 재생
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # 출력 비디오에 현재 프레임을 두 번 씩 작성
#         slow_video.write(frame)
#         slow_video.write(frame)

#     cap.release()

#     # then : 비디오 파일 유효성 확인
#     assert os.path.exists(SLOW_VIDEO_PATH)
