import torch
import json

from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_default_device("cuda")

# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2", torch_dtype="auto", trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)


for i, segment in enumerate(segments):
    text = segments[i]["translated_text"].replace(".", " ")
    inputs = tokenizer(
        "Instruct: Summarize this text as description of art painting in 8 words or less: '"
        + text
        + "'\nOutput:",
        return_tensors="pt",
        return_attention_mask=False,
    )
    outputs = model.generate(**inputs, max_length=200)

    text = tokenizer.batch_decode(outputs)[0]
    outputs = text.split("Output:")
    if len(outputs) > 2:
        text = outputs[1]
    else:
        text = outputs[-1]
    text = text.split("<|endoftext|>")[0].strip()

    segments[i]["summarized"] = text
    print(text)

# save segments to json file
with open("data/segments.json", "w") as f:
    json.dump(segments, f, indent=2, ensure_ascii=False)
