# whisper_gui_transcriber/conversion/ffmpeg_wrapper.py

import ffmpeg


def convert_mp4_to_wav(input_file, output_file):
    """
    使用 FFmpeg 將 MP4 檔案轉換為 WAV。
    :param input_file: 輸入的 MP4 檔案路徑
    :param output_file: 輸出的 WAV 檔案路徑
    """
    try:
        ffmpeg.input(input_file).output(
            output_file, format='wav').run(overwrite_output=True)
        print(f"已成功將 {input_file} 轉換為 {output_file}")
    except ffmpeg.Error as e:
        raise RuntimeError(f"轉換失敗：{e.stderr.decode('utf-8')}")
