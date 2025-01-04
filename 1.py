import whisper
import torch

import time

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

start_time = time.time()
result = model.transcribe("草東沒有派對 No Party For Cao Dong - 但 Damn【Official Video】.wav")
end_time = time.time()

print(f"轉錄完成，用時: {end_time - start_time:.2f} 秒，設備: {device}")
