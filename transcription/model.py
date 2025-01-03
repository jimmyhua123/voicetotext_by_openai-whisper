# whisper_gui_transcriber/transcription/model.py

import whisper

def load_whisper_model(model_size="base"):
    """
    載入 Whisper 模型。
    :param model_size: 模型大小，預設為 "base"
    :return: Whisper 模型實例
    """
    try:
        print(f"正在加載 {model_size} 模型...")
        model = whisper.load_model(model_size)
        print(f"{model_size} 模型加載成功！")
        return model
    except Exception as e:
        raise RuntimeError(f"加載模型失敗：{e}")
