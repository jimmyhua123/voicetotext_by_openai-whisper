# whisper_gui_transcriber/gui/app.py

import tkinter as tk
from .components import create_header, create_options, create_buttons, create_status, create_language_dropdown
from .events import handle_conversion, handle_transcription, quit_application


def run_app():
    root = tk.Tk()
    root.title("語音轉文字工具")
    root.geometry("600x600")
    root.resizable(False, False)
    root.configure(bg="#f0f8ff")

    # Header
    create_header(root)

    # Options
    include_timecodes_var, output_srt_var = create_options(root)

    # Language Dropdown
    selected_language, language_map = create_language_dropdown(root)

    # Status
    progress_label, timer_label = create_status(root)

    # Buttons
    create_buttons(
        root,
        include_timecodes_var,
        output_srt_var,
        progress_label,
        timer_label,
        selected_language,
        language_map
    )

    # Event to quit
    root.protocol("WM_DELETE_WINDOW", lambda: quit_application(root))

    root.mainloop()
