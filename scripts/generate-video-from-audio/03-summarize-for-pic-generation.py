import torch
import json

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

torch.set_default_device("cuda")

# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)
for i, segment in enumerate(segments):
    text = segments[i]["translated_text"].replace(".", " ")
    messages = [
        {
            "role": "user",
            "content": """
            Summarize this text in 5 words or less as movie title about alextime. 
            RESPOND ONLY WITH movie title AND NOTHING ELSE. DO NOT EXPLAIN YOUR REASONING.
            Text: `"""
            + text
            + "`",
        }
    ]

    generation_args = {
        "max_new_tokens": 500,
        "return_full_text": False,
        "temperature": 0.0,
        "do_sample": False,
    }
    output = pipe(messages, **generation_args)
    text = output[0]["generated_text"].strip()
    text = text.split("\n")[0] if len(text.split("\n")) > 0 else text
    text = text.replace('"', "")
    print(text)
    segments[i]["summary"] = text

# save segments to json file
with open("data/segments.json", "w") as f:
    json.dump(segments, f, indent=2, ensure_ascii=False)
