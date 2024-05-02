import json
from faster_whisper import WhisperModel

model_size = "medium"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

FILENAME = "2024-04-23"

segments, _ = model.transcribe(
    "./calls/" + FILENAME + ".m4a",
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
    language="ru",
)
data = []
for segment in segments:
    data.append({"start": segment.start, "end": segment.end, "text": segment.text})
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

# save segments to json file
with open("data/segments.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

text_combined = ". ".join([segment["text"] for segment in data])

with open("transcripts/" + FILENAME + ".txt", "w") as f:
    f.write(text_combined)
    f.close()
