# whisper_gui_transcriber/transcription/__init__.py

"""
轉錄模組，處理 Whisper 模型的載入與音訊轉錄邏輯。
包含轉錄過程中的輔助工具函數。
"""

from .model import load_whisper_model
from .transcription import transcribe_audio
from .utils import generate_unique_filename
