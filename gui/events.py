from tkinter import filedialog, messagebox
from threading import Thread, Event
import time
import os
import ffmpeg
from transcription.model import load_whisper_model
from transcription.transcription import transcribe_audio
from transcription.utils import generate_unique_filename
from conversion.ffmpeg_wrapper import convert_mp4_to_wav

# 定義全域停止事件
stop_event = Event()


def handle_conversion():
    video_file = filedialog.askopenfilename(
        title="選擇 MP4 影片檔案",
        filetypes=[("影片檔案", "*.mp4")]
    )
    if not video_file:
        messagebox.showinfo("取消", "未選擇影片檔案！")
        return

    try:
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        output_folder = "converted_audio"
        output_file = generate_unique_filename(
            output_folder, base_name, ".wav")
        convert_mp4_to_wav(video_file, output_file)
        messagebox.showinfo("完成", f"音訊已成功提取並儲存為：\n{output_file}")
    except Exception as e:
        messagebox.showerror("錯誤", f"轉換失敗：{e}")


def handle_transcription(include_timecodes, output_srt):
    audio_file = filedialog.askopenfilename(
        title="選擇音訊檔案",
        filetypes=[("音訊檔案", "*.mp3 *.wav *.flac *.m4a")]
    )
    if not audio_file:
        messagebox.showinfo("取消", "未選擇音訊檔案！")
        return

    try:
        # 開始轉錄過程
        model = load_whisper_model("base")
        transcribe_audio(
            model, audio_file, include_timecodes, output_srt,
            progress_callback=lambda text: print(f"進度：{text}"),
            timer_callback=lambda elapsed: print(f"花費時間：{elapsed} 秒")
        )
    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤：{e}")


def cancel_operation(progress_label, timer_label):
    """
    中止當前操作，並重置進度和計時器。
    :param progress_label: 用於顯示進度的標籤
    :param timer_label: 用於顯示計時器的標籤
    """
    stop_event.set()
    progress_label.config(text="操作已取消")
    reset_timer(timer_label)
    messagebox.showinfo("取消", "操作已成功中止")


def reset_timer(timer_label):
    """
    重置計時器的顯示。
    :param timer_label: 用於顯示計時器的標籤
    """
    timer_label.config(text="已花時間：0 分 0 秒")
    timer_label.update()


def quit_application(root):
    """
    結束應用程式。
    :param root: Tkinter 根窗口
    """
    stop_event.set()
    if messagebox.askyesno("結束應用", "確定要退出應用程式嗎？"):
        root.destroy()
