import json
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from faster_whisper import WhisperModel

model_size = "large-v2"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")


segments, _ = model.transcribe(
    "2023-10-19.mp3",
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
)
data = []
for segment in segments:
    data.append({"start": segment.start,
                "end": segment.end, "text": segment.text})
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

# save segments to json file
with open("data/segments.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
