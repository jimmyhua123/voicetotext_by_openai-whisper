# Whisper GUI Transcriber

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Attribution
This project utilizes the following open-source and commercial resources:
1. **[openai-whisper](https://github.com/openai/whisper)**: An open-source audio-to-text library by OpenAI, licensed under the MIT License.
2. **[OpenAI API](https://platform.openai.com/overview)**: Powered by OpenAI's GPT model for transcription and natural language processing tasks.

---

## English Version

### **Overview**
Whisper GUI Transcriber is a user-friendly application for converting audio files into text. Powered by OpenAI's Whisper model, this tool supports multiple audio formats and allows users to optionally include timestamps in the transcription.

---

### **Features**
1. **Multiple Audio Format Support**: Works with MP3, WAV, FLAC, and M4A.
2. **Timestamp Option**: Include time markers in the transcription.
3. **Real-time Progress**: Displays the current progress and elapsed time.
4. **One-click Dependency Installation**: Automatically installs required libraries.
5. **Multi-language Support**: Includes support for languages like English, Chinese, Japanese, etc.

---

### **Installation**
1. Install Python 3.7 or above.
2. Clone this repository:
   ```bash
   git clone https://github.com/jimmyhua123/voicetotext_by_openai-whisper.git
3. cd voicetotext_by_openai-whisper
4. pip install openai-whisper ffmpeg-python
5. Ensure FFmpeg is installed on your system:
Windows: choco install ffmpeg
MacOS: brew install ffmpeg
Ubuntu: sudo apt install ffmpeg

---

### **Usage**
1. Run the application:
   ```bash
   python main.py
   ```
2. Click "Install Dependencies" to install required libraries (if not already installed).
3. Select an audio file and optionally enable the "Include Timestamp" checkbox.
4. View real-time progress and elapsed time on the interface.
5. Once complete, the transcription file will be saved locally.

---

### **Credits**
- **Author**: Jimmy Hua  
- **GitHub**: [Whisper GUI Transcriber](https://github.com/jimmyhua123/voicetotext_by_openai-whisper/blob/main/whisper_gui_transcriber.py)
---

## 中文版本

### **概述**
Whisper GUI Transcriber 是一款用戶友好的語音轉文字工具，基於 OpenAI 的 Whisper 模型，支持多種音訊格式，並可選擇是否在逐字稿中包含時間碼。

---

### **功能特性**
1. **支持多種音訊格式**：適用於 MP3、WAV、FLAC 和 M4A。
2. **時間碼選項**：逐字稿中可包含時間標記。
3. **實時進度顯示**：界面顯示當前進度和已花時間。
4. **一鍵安裝套件**：自動安裝所需的軟體包。
5. **多語言支持** : 支持中文、英文、日文等多種語言。

---

### **安裝**
1. 安裝 Python 3.7 或更高版本。
2. 克隆此倉庫：
   ```bash
   git clone https://github.com/jimmyhua123/voicetotext_by_openai-whisper.git
   ```
3. 進入項目目錄：
   ```bash
   cd voicetotext_by_openai-whisper
   ```
4. 如需手動安裝套件：
   ```bash
   pip install openai-whisper ffmpeg-python
   ```
5. 確保系統已安裝 FFmpeg 工具：
   Windows: choco install ffmpeg
   MacOS: brew install ffmpeg
   Ubuntu: sudo apt install ffmpeg




---

### **使用方法**
1. 啟動應用：
   ```bash
   python main.py
   ```
2. 點擊 "安裝套件" 按鈕以安裝所需的軟體包（如尚未安裝）。
3. 選擇音訊文件，並根據需要啟用 "包含時間碼" 選項。
4. 界面會顯示實時進度和已花時間。
5. 完成後，下載生成的逐字稿文件。

---

### **致謝**
- **作者**: Jimmy Hua  
- **GitHub**: [Whisper GUI Transcriber](https://github.com/jimmyhua123/voicetotext_by_openai-whisper/blob/main/whisper_gui_transcriber.py)
