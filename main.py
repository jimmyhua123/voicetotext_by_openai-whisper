# whisper_gui_transcriber/main.py

from gui.app import run_app
import torch
import whisper

print("是否有可用的 GPU:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU 名稱:", torch.cuda.get_device_name(0))
else:
    print("使用 CPU 執行")

# 設置設備
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"正在使用設備: {device}")

# 加載模型時指定設備
model = whisper.load_model("base", device=device)

# 如果需要將模型傳遞到其他模組
# 將 `model` 傳遞給需要使用的函數

print(f"正在使用設備: {device}")
if __name__ == "__main__":
    run_app()


