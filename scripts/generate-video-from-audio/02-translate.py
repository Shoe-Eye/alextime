import json
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch

device = torch.device("cuda")


# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to(
    device
)

tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
tokenizer.src_lang = "ru"


for i, segment in enumerate(segments):
    encoded = tokenizer(segment["text"], return_tensors="pt").to(device)
    generated_tokens = model.generate(
        **encoded, forced_bos_token_id=tokenizer.get_lang_id("en")
    )
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    segments[i]["translated_text"] = translated_text[0]

# save segments to json file
with open("data/segments.json", "w") as f:
    json.dump(segments, f, indent=2, ensure_ascii=False)
