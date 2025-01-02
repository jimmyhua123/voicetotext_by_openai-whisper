import whisper
import tkinter as tk
from tkinter import filedialog, messagebox, BooleanVar, Checkbutton
import os
from threading import Thread
import subprocess
import time

def ensure_dependencies():
    try:
        subprocess.check_call(["pip", "install", "openai-whisper", "ffmpeg-python"])
        messagebox.showinfo("依賴安裝", "所有依賴已安裝完成！")
    except Exception as e:
        messagebox.showerror("錯誤", f"安裝依賴時發生錯誤：{e}")

def update_progress(progress_label, text):
    progress_label.config(text=text)
    progress_label.update()

def transcribe_audio(progress_label, include_timecodes):
    # 彈出檔案選擇對話框
    audio_file = filedialog.askopenfilename(
        title="選擇音訊檔案",
        filetypes=[("音訊檔案", "*.mp3 *.wav *.flac *.m4a")]
    )

    if not audio_file:
        messagebox.showinfo("取消", "未選擇音訊檔案！")
        return

    try:
        # 記錄開始時間
        start_time = time.time()

        # 加載 Whisper 模型
        update_progress(progress_label, "正在加載模型...")
        model = whisper.load_model("base")

        # 開始轉錄
        update_progress(progress_label, "正在轉錄音訊檔案...")
        result = model.transcribe(audio_file, word_timestamps=include_timecodes)

        # 將結果存成檔案
        output_file = os.path.splitext(audio_file)[0] + "_transcription.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            if include_timecodes:
                for segment in result['segments']:
                    start = segment['start']
                    end = segment['end']
                    text = segment['text']
                    f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
            else:
                f.write(result["text"])

        # 計算已花時間
        elapsed_time = time.time() - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)

        # 完成訊息
        update_progress(progress_label, "完成！逐字稿已儲存。")
        messagebox.showinfo("完成", f"逐字稿已儲存至：\n{output_file}\n已花時間：{int(elapsed_minutes)} 分 {int(elapsed_seconds)} 秒")
    except Exception as e:
        update_progress(progress_label, "發生錯誤")
        messagebox.showerror("錯誤", f"發生錯誤：{e}")
    finally:
        update_progress(progress_label, "")

def start_transcription(progress_label, include_timecodes):
    # 使用執行緒避免卡住界面
    Thread(target=transcribe_audio, args=(progress_label, include_timecodes)).start()

def install_dependencies():
    # 使用執行緒避免卡住界面
    Thread(target=ensure_dependencies).start()

# 建立主視窗
root = tk.Tk()
root.title("語音轉文字工具")
root.geometry("400x350")

# 介面標籤
label = tk.Label(root, text="選擇音訊檔案以生成逐字稿", font=("Arial", 12))
label.pack(pady=20)

# 進度標籤
progress_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
progress_label.pack(pady=10)

# 是否包含時間碼
include_timecodes_var = BooleanVar()
timecode_checkbox = Checkbutton(root, text="包含時間碼", font=("Arial", 10), variable=include_timecodes_var)
timecode_checkbox.pack(pady=10)

# 安裝依賴按鈕
install_button = tk.Button(root, text="安裝依賴", font=("Arial", 14), command=install_dependencies)
install_button.pack(pady=10)

# 選擇檔案按鈕
select_button = tk.Button(root, text="選擇檔案", font=("Arial", 14), command=lambda: start_transcription(progress_label, include_timecodes_var.get()))
select_button.pack(pady=10)

# 啟動主迴圈
root.mainloop()
