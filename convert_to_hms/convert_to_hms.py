import os
import re
from datetime import timedelta

def convert_to_hms(seconds):
    """將秒數轉換為時/分/秒格式"""
    td = timedelta(seconds=seconds)
    return str(td).split('.')[0]  # 去掉毫秒部分

def process_file(input_file):
    """處理單一檔案並輸出轉換結果"""
    # 加入完整路徑
    input_file_path = os.path.join(current_dir, input_file)
    output_file_path = f"{os.path.splitext(input_file_path)[0]}_converted.txt"
    with open(input_file_path, "r", encoding="utf-8") as infile, open(output_file_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            # 使用正則表達式提取時間碼
            match = re.match(r'\[(\d+\.\d+) - (\d+\.\d+)\] (.+)', line)
            if match:
                start_sec, end_sec, text = match.groups()
                start_hms = convert_to_hms(float(start_sec))
                end_hms = convert_to_hms(float(end_sec))
                outfile.write(f"[{start_hms} - {end_hms}] {text}\n")
            else:
                # 如果沒有時間碼，直接寫入
                outfile.write(line)
    print(f"已轉換: {input_file_path} -> {output_file_path}")

def main():
    """處理當前資料夾內的所有 .txt 檔案"""
    global current_dir  # 宣告全域變數
    current_dir = os.path.dirname(os.path.abspath(__file__))
    txt_files = [f for f in os.listdir(current_dir) if f.endswith('.txt')]

    if not txt_files:
        print("未找到任何 .txt 檔案")
        return

    print("開始轉換 .txt 檔案...")
    for txt_file in txt_files:
        process_file(txt_file)
    print("所有檔案處理完成！")

if __name__ == "__main__":
    main()
