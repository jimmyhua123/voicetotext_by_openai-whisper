# whisper_gui_transcriber/transcription/utils.py

import os


def generate_unique_filename(folder, base_name, extension):
    """
    生成唯一的檔案名稱，避免覆蓋現有檔案。
    :param folder: 儲存檔案的資料夾路徑
    :param base_name: 檔案基礎名稱（不含副檔名）
    :param extension: 檔案副檔名（如 ".txt" 或 ".srt"）
    :return: 唯一的檔案路徑
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    counter = 1
    while os.path.exists(os.path.join(folder, f"{base_name}_{counter}{extension}")):
        counter += 1

    return os.path.join(folder, f"{base_name}_{counter}{extension}")
