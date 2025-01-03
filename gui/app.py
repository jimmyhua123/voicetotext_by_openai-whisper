import tkinter as tk
from gui.components import create_header, create_options, create_buttons, create_status, create_language_dropdown
from gui.events import handle_conversion, handle_transcription, quit_application
import webbrowser


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

    # Add footer with author and GitHub link
    add_footer(root)

    # Event to quit
    root.protocol("WM_DELETE_WINDOW", lambda: quit_application(root))

    root.mainloop()


def add_footer(root):
    """
    在視窗底部添加作者資訊與 GitHub 連結。
    """
    footer_frame = tk.Frame(root, bg="#f0f8ff")
    footer_frame.pack(side=tk.BOTTOM, pady=5)

    # 作者資訊
    author_label = tk.Label(
        footer_frame,
        text="Made by Jimmy Hua",
        font=("Arial", 10, "italic"),
        bg="#f0f8ff",
        fg="#555"
    )
    author_label.grid(row=0, column=0, padx=5, sticky="w")

    # GitHub 連結
    github_label = tk.Label(
        footer_frame,
        text="GitHub: voicetotext_by_openai-whisper",
        font=("Arial", 10, "underline"),
        bg="#f0f8ff",
        fg="blue",
        cursor="hand2"
    )
    github_label.grid(row=1, column=0, padx=5, sticky="w")

    # 點擊 GitHub 連結時開啟瀏覽器
    github_label.bind("<Button-1>", lambda e: open_github(
        "https://github.com/jimmyhua123/voicetotext_by_openai-whisper"
    ))

def open_github(url):
    """
    開啟指定的 GitHub 頁面。
    """
    webbrowser.open_new_tab(url)
