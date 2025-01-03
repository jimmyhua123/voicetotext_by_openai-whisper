# whisper_gui_transcriber/conversion/__init__.py

"""
格式轉換模組，處理與音訊或影片格式相關的邏輯。
包含與 FFmpeg 的整合與輔助工具函數。
"""

from .ffmpeg_wrapper import convert_mp4_to_wav
from .utils import ensure_folder_exists
