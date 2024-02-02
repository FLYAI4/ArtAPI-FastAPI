import os
from dotenv import load_dotenv

focus_point_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
libs_path = os.path.abspath(os.path.join(focus_point_path, os.path.pardir))
load_dotenv(libs_path)
