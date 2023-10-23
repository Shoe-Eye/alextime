import os
import json
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from faster_whisper import WhisperModel

model_size = "large-v2"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

files = os.listdir("./calls/")
audio_files = [file for file in files if file.endswith(
    ".mp3") or file.endswith(".m4a") or file.endswith(".ogg")]


for file in audio_files:

    segments, _ = model.transcribe(
        "./calls/" + file,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )
    text = " ".join([segment.text for segment in segments])
    # save segments to json file
    with open("transcripts/" + file + ".txt", "w") as f:
        json.dump(text, f, indent=2, ensure_ascii=False)
