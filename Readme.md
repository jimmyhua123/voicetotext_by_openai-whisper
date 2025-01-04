以下是更新的 `Readme.md`，包含使用 GPU 執行程序時需要安裝的套件和相關步驟。

---

### 更新後的 **Readme.md**

```markdown
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
4. **Multi-language Support**: Includes support for languages like English, Chinese, Japanese, etc.

---

### **Installation**
1. Install Python 3.7 or higher. After testing, Python 3.13 is not supported. I am using Python 3.11.1.
2. Clone this repository:
   ```bash
   git clone https://github.com/jimmyhua123/voicetotext_by_openai-whisper.git
   ```
3. Navigate to the project directory:
   ```bash
   cd voicetotext_by_openai-whisper
   ```
4. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. **Using GPU for Acceleration**:
   - Ensure your system has a **NVIDIA GPU** with CUDA installed.
   - Install the following additional Python packages:
     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```
     - Replace `cu118` with the appropriate version for your CUDA installation.
   - Confirm GPU availability in Python:
     ```python
     import torch
     print("是否有可用的 GPU:", torch.cuda.is_available())
     if torch.cuda.is_available():
         print("GPU 名稱:", torch.cuda.get_device_name(0))
     ```
   - Install **FFmpeg** on your system:
     - **Windows**: `choco install ffmpeg`
     - **MacOS**: `brew install ffmpeg`
     - **Ubuntu**: `sudo apt install ffmpeg`

---

### **Usage**
1. Run the application:
   ```bash
   python main.py
   ```
2. Select an audio file and optionally enable the "Include Timestamp" checkbox.
3. View real-time progress and elapsed time on the interface.
4. Once complete, the transcription file will be saved locally.

---

### **Credits**
- **Author**: Jimmy Hua  
- **GitHub**: [Whisper GUI Transcriber](https://github.com/jimmyhua123/voicetotext_by_openai-whisper)

---

## 中文版本

### **概述**
Whisper GUI Transcriber 是一款用戶友好的語音轉文字工具，基於 OpenAI 的 Whisper 模型，支持多種音訊格式，並可選擇是否在逐字稿中包含時間碼。

---

### **功能特性**
1. **支持多種音訊格式**：適用於 MP3、WAV、FLAC 和 M4A。
2. **時間碼選項**：逐字稿中可包含時間標記。
3. **實時進度顯示**：界面顯示當前進度和已花時間。
4. **多語言支持** : 支持中文、英文、日文等多種語言。

---

### **安裝**
1. 安裝 Python 3.7 或更高版本 經測試Python 3.13 不行 我是用 Python3.11.1。
2. 克隆此倉庫：
   ```bash
   git clone https://github.com/jimmyhua123/voicetotext_by_openai-whisper.git
   ```
3. 進入項目目錄：
   ```bash
   cd voicetotext_by_openai-whisper
   ```
4. 安裝所需的 Python 套件：
   ```bash
   pip install -r requirements.txt
   ```

5. **啟用 GPU 加速**：
   - 確保你的系統有 **NVIDIA GPU** 並已安裝 CUDA 工具包。
   - 安裝以下 Python 套件：
     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```
     - 根據你的 CUDA 版本調整 `cu118`。
   - 在 Python 中確認 GPU 狀態：
     ```python
     import torch
     print("是否有可用的 GPU:", torch.cuda.is_available())
     if torch.cuda.is_available():
         print("GPU 名稱:", torch.cuda.get_device_name(0))
     ```

6. 確保系統已安裝 FFmpeg 工具：
   - **Windows**: `choco install ffmpeg`
   - **MacOS**: `brew install ffmpeg`
   - **Ubuntu**: `sudo apt install ffmpeg`

---

### **使用方法**
1. 啟動應用：
   ```bash
   python main.py
   ```
2. 選擇音訊文件，並根據需要啟用 "包含時間碼" 選項。
3. 界面會顯示實時進度和已花時間。
4. 完成後，生成的逐字稿文件將儲存於本地。

---

### **致謝**
- **作者**: Jimmy Hua  
- **GitHub**: [Whisper GUI Transcriber](https://github.com/jimmyhua123/voicetotext_by_openai-whisper)
```

---

### 更新內容
1. **增加了 GPU 相關安裝指引**：
   - 說明如何安裝 `torch` 支持 CUDA。
   - 提供驗證 GPU 是否可用的代碼。

2. **完整的 FFmpeg 安裝方法**：
   - 提供適用於不同操作系統的安裝指令。

3. **與中文版本同步的安裝步驟**。

如果還有其他需求，請隨時告訴我！ 😊