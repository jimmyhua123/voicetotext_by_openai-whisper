# whisper_gui_transcriber/transcription/transcription.py

import os
import time
from transcription.utils import generate_unique_filename


def transcribe_audio(model, audio_file, include_timecodes, output_srt, progress_callback=None, timer_callback=None):
    """
    使用 Whisper 模型轉錄音訊。
    :param model: Whisper 模型實例
    :param audio_file: 音訊檔案路徑
    :param include_timecodes: 是否包含時間碼
    :param output_srt: 是否輸出為 SRT 字幕檔
    :param progress_callback: 回報進度的函數
    :param timer_callback: 回報計時器更新的函數
    """
    try:
        start_time = time.time()

        if progress_callback:
            progress_callback("正在加載音訊檔案...")

        # 開始轉錄音訊
        result = model.transcribe(
            audio_file,
            word_timestamps=include_timecodes,
            language="zh"  # 強制指定中文
        )

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

                    f.write(f"[{start:.2f} - {end:.2f}] {text}\n")

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

        elapsed_time = time.time() - start_time
        if timer_callback:
            timer_callback(elapsed_time)

        if progress_callback:
            progress_callback("轉錄完成，檔案已儲存。")

        print(f"檔案已儲存至：{output_file}")
    except Exception as e:
        if progress_callback:
            progress_callback("轉錄過程中發生錯誤。")
        raise RuntimeError(f"轉錄失敗：{e}")
