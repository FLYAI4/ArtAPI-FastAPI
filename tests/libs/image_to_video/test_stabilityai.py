import os
import time
import cv2
import pytest
import requests
from dotenv import load_dotenv
from PIL import Image
from src.libs.image_to_video.stabilityai import VideoManager
from src.libs.api.exception import ImageToVideoError

# Setting
load_dotenv()
focus_point_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_folder_path = os.path.abspath(os.path.join(focus_point_path, "test_img"))

# Mockup
IMG_PATH = os.path.abspath(os.path.join(test_img_folder_path, "origin_img.jpg"))
SEED = 0
CFG_SCALE = 2.5
MOTION_BUCKET_ID=40
GENERATED_ID="f7777dd518ca42a4ff642f5cd979e1d2e8611548a76b154a396d974f9077c37b"
GENERATE_ORIGIN_VIDEO_PATH = os.path.abspath(os.path.join(test_img_folder_path, "origin_video.mp4"))
REVERSED_VIDEO_PATH = os.path.abspath(os.path.join(test_img_folder_path, "reversed_video.mp4"))
SLOW_VIDEO_PATH = os.path.abspath(os.path.join(test_img_folder_path, "slow_video.mp4"))


# @pytest.mark.order(1)
# @pytest.mark.asyncio
# async def test_can_resize_image():
#     # given : 유효한 이미지
#     # when : 이미지 사이즈 변경 요청
#     resize_image_path = VideoManager(test_img_folder_path).resize_image("origin_img.jpg")

#     # then : 이미지 저장 파일 확인
#     assert os.path.exists(resize_image_path)

# TODO: token 사용량 때문에 실행 제외
# @pytest.mark.order(2)
# @pytest.mark.asyncio
# async def test_can_request_generate_video():
#     # given : 유효한 토큰 + 이미지
#     # RESIZED_IMAGE_PATH = os.path.abspath(os.path.join(test_img_folder_path, "resized_img.jpg"))
#     # when : 비디오 생성 요청
#     response = VideoManager(test_img_folder_path).post_generated_video("resized_img.jpg")
#     print(response.json())
#     assert response.status_code == 200
#     assert len(response.json()["id"]) > 0

# @pytest.mark.order(2)
# @pytest.mark.asyncio
# async def test_cannot_request_generate_video_with_non_token():
#     # given : 잘못된 토큰 + 이미지
#     NO_TOKEN_ID_KEY = "wrong_token"

#     # then : error
#     with pytest.raises(ImageToVideoError):
#         # when : 비디오 생성 요청
#         response = VideoManager(test_img_folder_path,
#                                 token=NO_TOKEN_ID_KEY).post_generated_video("resized_img.jpg")
#         assert response.status_code == 200


# @pytest.mark.order(3)
# @pytest.mark.asyncio
# async def test_can_get_generated_video():
#     # given : 생성된 비디오 요청 id
#     # when : 비디오 전달 요청
#     generated_origin_path = VideoManager(
#         test_img_folder_path).get_generated_video(GENERATED_ID, "origin_video.mp4")

#     # then : 비디오 전달 확인
#     assert os.path.exists(generated_origin_path)


# @pytest.mark.order(4)
# @pytest.mark.asyncio
# async def test_can_reverse_generated_video():
#     # given : 유효한 비디오 파일
#     # when : 비디오 파일 역 재생 및 연결
#     # 비디오 속성 가져오기
#     reversed_video_path = VideoManager(test_img_folder_path).reverse_generated_video(GENERATE_ORIGIN_VIDEO_PATH, "reversed_video.mp4")

#     # then : 비디오 파일 유효성 확인
#     assert os.path.exists(reversed_video_path)


@pytest.mark.order(5)
def test_can_slow_generated_video():
    # given : 유효한 비디오 파일
    # when : 비디오 파일 역 재생 및 연결
    # 비디오 속성 가져오기
    slow_video_path = VideoManager(test_img_folder_path).slow_generated_video(REVERSED_VIDEO_PATH, "slow_video.mp4")

    # then : 비디오 파일 유효성 확인
    assert os.path.exists(slow_video_path)
