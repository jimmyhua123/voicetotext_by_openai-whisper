# whisper_gui_transcriber/conversion/utils.py

import os


def ensure_folder_exists(folder):
    """
    確保指定資料夾存在，不存在則建立。
    :param folder: 資料夾路徑
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"資料夾 {folder} 已建立。")
    else:
        print(f"資料夾 {folder} 已存在。")
