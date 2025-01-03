# whisper_gui_transcriber/gui/components.py

import tkinter as tk
from tkinter import BooleanVar, Checkbutton


def create_header(root):
    header_frame = tk.Frame(root, bg="#f0f8ff")
    header_frame.pack(pady=10)

    label = tk.Label(header_frame, text="語音轉文字工具", font=(
        "Arial", 20, "bold"), bg="#f0f8ff", fg="#333")
    label.grid(row=0, column=0, pady=5)

    subtitle_label1 = tk.Label(header_frame, text="選擇音訊檔案以生成逐字稿或字幕", font=(
        "Arial", 12), bg="#f0f8ff", fg="#555")
    subtitle_label1.grid(row=1, column=0)

    subtitle_label2 = tk.Label(header_frame, text="mp4需先轉成wav或mp3", font=(
        "Arial", 12), bg="#f0f8ff", fg="#555")
    subtitle_label2.grid(row=2, column=0)


def create_options(root):
    options_frame = tk.Frame(root, bg="#f0f8ff")
    options_frame.pack(pady=20)

    include_timecodes_var = BooleanVar()
    timecode_checkbox = Checkbutton(
        options_frame,
        text="包含時間碼",
        font=("Arial", 12),
        variable=include_timecodes_var,
        bg="#f0f8ff",
        activebackground="#e6f7ff"
    )
    timecode_checkbox.grid(row=0, column=0, padx=10, pady=5)

    output_srt_var = BooleanVar()
    srt_checkbox = Checkbutton(
        options_frame,
        text="輸出為 .srt 字幕檔",
        font=("Arial", 12),
        variable=output_srt_var,
        bg="#f0f8ff",
        activebackground="#e6f7ff"
    )
    srt_checkbox.grid(row=0, column=1, padx=10, pady=5)

    return include_timecodes_var, output_srt_var


def create_buttons(root, include_timecodes_var, output_srt_var, progress_label, timer_label):
    from .events import handle_conversion, handle_transcription, cancel_operation, quit_application

    button_frame = tk.Frame(root, bg="#f0f8ff")
    button_frame.pack(pady=20)

    convert_button = tk.Button(
        button_frame,
        text="轉換 MP4 為 WAV",
        font=("Arial", 14),
        bg="#28a745",
        fg="white",
        activebackground="#1e7e34",
        activeforeground="white",
        command=handle_conversion
    )
    convert_button.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5)

    select_audio_button = tk.Button(
        button_frame,
        text="選擇音訊檔案並執行",
        font=("Arial", 14),
        bg="#007acc",
        fg="white",
        activebackground="#005f99",
        activeforeground="white",
        command=lambda: handle_transcription(
            include_timecodes_var.get(), output_srt_var.get()
        )
    )
    select_audio_button.grid(row=0, column=1, padx=10,
                             pady=10, ipadx=10, ipady=5)

    cancel_button = tk.Button(
        button_frame,
        text="取消執行",
        font=("Arial", 14),
        bg="#ffc107",
        fg="black",
        activebackground="#d39e00",
        activeforeground="black",
        command=lambda: cancel_operation(progress_label, timer_label)
    )
    cancel_button.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=5)

    quit_button = tk.Button(
        button_frame,
        text="結束",
        font=("Arial", 14),
        bg="#dc3545",
        fg="white",
        activebackground="#bd2130",
        activeforeground="white",
        command=lambda: quit_application(root)
    )
    quit_button.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=5)


def create_status(root):
    status_frame = tk.Frame(root, bg="#f0f8ff")
    status_frame.pack(pady=10)

    progress_label = tk.Label(
        status_frame,
        text="",
        font=("Arial", 10),
        bg="#f0f8ff",
        fg="blue"
    )
    progress_label.grid(row=0, column=0, pady=5)

    timer_label = tk.Label(
        status_frame,
        text="已花時間：0 分 0 秒",
        font=("Arial", 10),
        bg="#f0f8ff",
        fg="green"
    )
    timer_label.grid(row=1, column=0, pady=5)

    return progress_label, timer_label
