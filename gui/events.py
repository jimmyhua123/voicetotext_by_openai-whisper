from tkinter import filedialog, messagebox
from threading import Thread, Event
import time
import os
from transcription.model import load_whisper_model
from transcription.transcription import transcribe_audio
from transcription.utils import generate_unique_filename
from conversion.ffmpeg_wrapper import convert_mp4_to_wav

# 定義全域停止事件
stop_event = Event()


def start_timer(timer_label):
    """
    啟動計時器。
    :param timer_label: 顯示計時的標籤
    """
    stop_event.clear()
    start_time = time.time()

    def timer_thread():
        while not stop_event.is_set():
            elapsed_time = time.time() - start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            timer_label.config(text=f"已花時間：{minutes} 分 {seconds} 秒")
            timer_label.update()
            time.sleep(1)

    Thread(target=timer_thread, daemon=True).start()


def reset_timer(timer_label):
    """
    重置計時器的顯示。
    :param timer_label: 用於顯示計時器的標籤
    """
    timer_label.config(text="已花時間：0 分 0 秒")
    timer_label.update()


def handle_conversion(timer_label, progress_label):
    """
    處理 MP4 到 WAV 的轉換邏輯。
    :param timer_label: 用於顯示計時的標籤
    :param progress_label: 用於顯示進度的標籤
    """
    video_file = filedialog.askopenfilename(
        title="選擇 MP4 影片檔案",
        filetypes=[("影片檔案", "*.mp4")]
    )
    if not video_file:
        messagebox.showinfo("取消", "未選擇影片檔案！")
        return

    try:
        start_timer(timer_label)
        progress_label.config(text="正在轉換 MP4 為 WAV...")
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        output_folder = "converted_audio"
        output_file = generate_unique_filename(
            output_folder, base_name, ".wav")
        convert_mp4_to_wav(video_file, output_file)
        progress_label.config(text="轉換完成！")
        messagebox.showinfo("完成", f"音訊已成功提取並儲存為：\n{output_file}")
    except Exception as e:
        messagebox.showerror("錯誤", f"轉換失敗：{e}")
    finally:
        stop_event.set()
        reset_timer(timer_label)
        progress_label.config(text="")


def handle_transcription(include_timecodes, output_srt, timer_label, progress_label):
    """
    處理音訊轉錄的邏輯。
    :param include_timecodes: 是否包含時間碼
    :param output_srt: 是否輸出為 SRT 格式
    :param timer_label: 用於顯示計時的標籤
    :param progress_label: 用於顯示進度的標籤
    """
    audio_file = filedialog.askopenfilename(
        title="選擇音訊檔案",
        filetypes=[("音訊檔案", "*.mp3 *.wav *.flac *.m4a")]
    )
    if not audio_file:
        messagebox.showinfo("取消", "未選擇音訊檔案！")
        return

    try:
        start_timer(timer_label)
        progress_label.config(text="正在加載模型...")
        model = load_whisper_model("base")
        progress_label.config(text="正在轉錄音訊檔案...")
        transcribe_audio(model, audio_file, include_timecodes, output_srt)
        progress_label.config(text="轉錄完成！")
        messagebox.showinfo("完成", "音訊轉錄已成功完成，檔案已儲存！")
    except Exception as e:
        messagebox.showerror("錯誤", f"轉錄失敗：{e}")
    finally:
        stop_event.set()
        reset_timer(timer_label)
        progress_label.config(text="")


def cancel_operation(timer_label, progress_label):
    """
    中止當前操作，並重置進度和計時器。
    :param timer_label: 用於顯示計時器的標籤
    :param progress_label: 用於顯示進度的標籤
    """
    stop_event.set()
    progress_label.config(text="操作已取消")
    reset_timer(timer_label)
    messagebox.showinfo("取消", "操作已成功中止")


def quit_application(root):
    """
    結束應用程式。
    :param root: Tkinter 根窗口
    """
    stop_event.set()
    if messagebox.askyesno("結束應用", "確定要退出應用程式嗎？"):
        root.destroy()
