import whisper
import tkinter as tk
from tkinter import filedialog, messagebox, BooleanVar, Checkbutton
import os
from threading import Thread, Event
import subprocess
import time
import ffmpeg

# 定義全域停止事件
stop_event = Event()

def ensure_dependencies():
    try:
        subprocess.check_call(
            ["pip", "install", "openai-whisper", "ffmpeg-python"])
        messagebox.showinfo("套件安裝", "所有套件已安裝完成！")
    except Exception as e:
        messagebox.showerror("錯誤", f"安裝套件時發生錯誤：{e}")

def update_progress(progress_label, text):
    progress_label.config(text=text)
    progress_label.update()

def update_timer(timer_label, start_time):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
        timer_label.config(
            text=f"已花時間：{int(elapsed_minutes)} 分 {int(elapsed_seconds)} 秒")
        time.sleep(1)

def generate_unique_filename(folder, base_name, extension):
    counter = 1
    if not os.path.exists(folder):
        os.makedirs(folder)
    while os.path.exists(os.path.join(folder, f"{base_name}_{counter}{extension}")):
        counter += 1
    return os.path.join(folder, f"{base_name}_{counter}{extension}")

def convert_mp4_to_wav():
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
        output_file = generate_unique_filename(output_folder, base_name, ".wav")

        ffmpeg.input(video_file).output(output_file, format='wav').run()

        messagebox.showinfo("完成", f"音訊已成功提取並儲存為：\n{output_file}")
    except Exception as e:
        messagebox.showerror("錯誤", f"轉換失敗：{e}")

def transcribe_audio(progress_label, timer_label, include_timecodes, output_srt):
    audio_file = filedialog.askopenfilename(
        title="選擇音訊檔案",
        filetypes=[("音訊檔案", "*.mp3 *.wav *.flac *.m4a")]
    )

    if not audio_file:
        messagebox.showinfo("取消", "未選擇音訊檔案！")
        return

    try:
        start_time = time.time()
        timer_thread = Thread(target=update_timer, args=(
            timer_label, start_time), daemon=True)
        timer_thread.start()

        update_progress(progress_label, "正在加載模型...")
        model = whisper.load_model("base")

        update_progress(progress_label, "正在轉錄音訊檔案...")
        result = model.transcribe(
            audio_file, word_timestamps=include_timecodes)

        base_name = os.path.splitext(os.path.basename(audio_file))[0]

        if output_srt:
            folder = "srt_files"
            srt_file = generate_unique_filename(folder, base_name, ".srt")
            with open(srt_file, "w", encoding="utf-8") as f:
                for segment in result['segments']:
                    start = segment['start']
                    end = segment['end']
                    text = segment['text']

                    start_timecode = time.strftime('%H:%M:%S', time.gmtime(start)) + f",{int((start % 1) * 1000):03d}"
                    end_timecode = time.strftime('%H:%M:%S', time.gmtime(end)) + f",{int((end % 1) * 1000):03d}"

                    f.write(f"{segment['id'] + 1}\n{start_timecode} --> {end_timecode}\n{text}\n\n")

            output_file = srt_file
        else:
            folder = "transcriptions_with_timecodes" if include_timecodes else "transcriptions_without_timecodes"
            txt_file = generate_unique_filename(folder, base_name, ".txt")
            with open(txt_file, "w", encoding="utf-8") as f:
                if include_timecodes:
                    for segment in result['segments']:
                        start = segment['start']
                        end = segment['end']
                        text = segment['text']
                        f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
                else:
                    f.write(result["text"])

            output_file = txt_file

        elapsed_time = time.time() - start_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)

        update_progress(progress_label, "完成！檔案已儲存。")
        messagebox.showinfo(
            "完成", f"檔案已儲存至：\n{output_file}\n已花時間：{int(elapsed_minutes)} 分 {int(elapsed_seconds)} 秒")
    except Exception as e:
        update_progress(progress_label, "發生錯誤")
        messagebox.showerror("錯誤", f"發生錯誤：{e}")
    finally:
        stop_event.clear()
        update_progress(progress_label, "")
        timer_label.config(text="")

def start_audio_transcription(progress_label, timer_label, include_timecodes, output_srt):
    stop_event.clear()
    Thread(target=transcribe_audio, args=(
        progress_label, timer_label, include_timecodes, output_srt)).start()

def toggle_checkboxes(*checkbox_vars):
    for var in checkbox_vars:
        var.set(False)

def install_dependencies():
    Thread(target=ensure_dependencies).start()

def cancel_operation():
    stop_event.set()
    messagebox.showinfo("取消", "操作已取消")

def quit_application():
    stop_event.set()
    root.destroy()

root = tk.Tk()
root.title("語音轉文字工具")
root.geometry("600x600")
root.resizable(False, False)
root.configure(bg="#f0f8ff")

header_frame = tk.Frame(root, bg="#f0f8ff")
header_frame.pack(pady=10)

label = tk.Label(header_frame, text="語音轉文字工具", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#333", borderwidth=0, highlightthickness=0)
label.grid(row=0, column=0, pady=5)

subtitle_label = tk.Label(header_frame, text="選擇音訊檔案以生成逐字稿或字幕", font=("Arial", 12), bg="#f0f8ff", fg="#555", borderwidth=0, highlightthickness=0)
subtitle_label.grid(row=1, column=0)
subtitle_label = tk.Label(header_frame, text="mp4需先轉成wav or mp3", font=("Arial", 12), bg="#f0f8ff", fg="#555", borderwidth=0, highlightthickness=0)
subtitle_label.grid(row=2, column=0)
options_frame = tk.Frame(root, bg="#f0f8ff")
options_frame.pack(pady=20)

include_timecodes_var = BooleanVar()
def on_include_timecodes_toggle():
    if include_timecodes_var.get():
        toggle_checkboxes(output_srt_var)
timecode_checkbox = Checkbutton(options_frame, text="包含時間碼", font=("Arial", 12), variable=include_timecodes_var,
                                 command=on_include_timecodes_toggle, bg="#f0f8ff", activebackground="#e6f7ff")
timecode_checkbox.grid(row=0, column=0, padx=10, pady=5)

output_srt_var = BooleanVar()
def on_output_srt_toggle():
    if output_srt_var.get():
        toggle_checkboxes(include_timecodes_var)
srt_checkbox = Checkbutton(options_frame, text="輸出為 .srt 字幕檔", font=("Arial", 12), variable=output_srt_var,
                            command=on_output_srt_toggle, bg="#f0f8ff", activebackground="#e6f7ff")
srt_checkbox.grid(row=0, column=1, padx=10, pady=5)

button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=20)

convert_button = tk.Button(button_frame, text="轉換 MP4 為 WAV", font=("Arial", 14), bg="#28a745", fg="white",
                            activebackground="#1e7e34", activeforeground="white", command=convert_mp4_to_wav)
convert_button.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5)

select_audio_button = tk.Button(button_frame, text="選擇音訊檔案並執行", font=("Arial", 14), bg="#007acc", fg="white",
                                 activebackground="#005f99", activeforeground="white", command=lambda: start_audio_transcription(progress_label, timer_label, include_timecodes_var.get(), output_srt_var.get()))
select_audio_button.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=5)

cancel_button = tk.Button(button_frame, text="取消執行", font=("Arial", 14), bg="#ffc107", fg="black",
                           activebackground="#d39e00", activeforeground="black", command=cancel_operation)
cancel_button.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=5)

quit_button = tk.Button(button_frame, text="結束", font=("Arial", 14), bg="#dc3545", fg="white",
                        activebackground="#bd2130", activeforeground="white", command=quit_application)
quit_button.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=5)

status_frame = tk.Frame(root, bg="#f0f8ff")
status_frame.pack(pady=10)

progress_label = tk.Label(status_frame, text="", font=("Arial", 10), bg="#f0f8ff", fg="blue", borderwidth=0, highlightthickness=0)
progress_label.grid(row=0, column=0, pady=5)

timer_label = tk.Label(status_frame, text="", font=("Arial", 10), bg="#f0f8ff", fg="green", borderwidth=0, highlightthickness=0)
timer_label.grid(row=1, column=0, pady=5)

footer_frame = tk.Frame(root, bg="#f0f8ff")
footer_frame.pack(pady=20)

author_label = tk.Label(footer_frame, text="Made by Jimmy Hua", font=("Arial", 10, "italic"), bg="#f0f8ff", fg="#333", borderwidth=0, highlightthickness=0)
author_label.grid(row=0, column=0)

github_label = tk.Label(footer_frame, text="GitHub: voicetotext_by_openai-whisper",
                        font=("Arial", 10, "underline"), bg="#f0f8ff", fg="#007acc", cursor="hand2", borderwidth=0, highlightthickness=0)
github_label.grid(row=1, column=0)
github_label.bind("<Button-1>", lambda e: os.system(
    "start https://github.com/jimmyhua123/voicetotext_by_openai-whisper/blob/main/whisper_gui_transcriber.py"))

root.mainloop()
