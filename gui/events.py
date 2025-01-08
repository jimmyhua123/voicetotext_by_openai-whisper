from tkinter import filedialog, messagebox
from threading import Thread, Event
import time
import os
from transcription.model import load_whisper_model
from transcription.transcription import transcribe_audio
from transcription.utils import generate_unique_filename
from conversion.ffmpeg_wrapper import convert_mp4_to_wav
import subprocess
from tkinter import messagebox


# 定義全域停止事件
stop_event = Event()


def start_timer(timer_label):
    """
    啟動計時器，並讓時間即時更新。
    :param timer_label: 顯示計時的標籤
    """
    stop_event.clear()
    start_time = time.time()

    def timer_thread():
        while not stop_event.is_set():
            elapsed_time = time.time() - start_time
            hours, remainder = divmod(int(elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_label.config(text=f"已花時間：{hours} 小時 {minutes} 分 {seconds} 秒")
            timer_label.update()
            time.sleep(1)  # 每秒更新一次

    Thread(target=timer_thread, daemon=True).start()


def reset_timer(timer_label):
    """
    重置計時器的顯示。
    :param timer_label: 用於顯示計時器的標籤
    """
    timer_label.config(text="已花時間：0 小時 0 分 0 秒")
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


def handle_transcription(include_timecodes, output_srt, language, timer_label, progress_label):

    if language == "auto":  # 如果選擇了 "自動檢測"
        language = None  # Whisper 自動檢測語言時需要傳遞 None
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
        result = model.transcribe(
            audio_file, language=language, word_timestamps=include_timecodes)

        # 儲存結果
        base_name = os.path.splitext(os.path.basename(audio_file))[0]

        if output_srt:
            folder = "srt_files"
            output_file = generate_unique_filename(folder, base_name, ".srt")
            with open(output_file, "w", encoding="utf-8") as f:
                for segment in result['segments']:
                    start = segment['start']
                    end = segment['end']
                    text = segment['text']
                    start_timecode = time.strftime(
                        '%H/%M/%S', time.gmtime(start)) + f",{int((start % 1) * 1000):03d}"
                    end_timecode = time.strftime(
                        '%H/%M/%S', time.gmtime(end)) + f",{int((end % 1) * 1000):03d}"

                    f.write(
                        f"{segment['id'] + 1}\n{start_timecode} --> {end_timecode}\n{text}\n\n")
        else:
            folder = "transcriptions_with_timecodes" if include_timecodes else "transcriptions_without_timecodes"
            output_file = generate_unique_filename(folder, base_name, ".txt")
            with open(output_file, "w", encoding="utf-8") as f:
                if include_timecodes:
                    for segment in result['segments']:
                        start = segment['start']
                        end = segment['end']
                        text = segment['text']
                        f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
                else:
                    f.write(result["text"])

        progress_label.config(text="轉錄完成！")
        messagebox.showinfo("完成", f"檔案已儲存至：\n{output_file}")
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
