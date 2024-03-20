import glob
import os
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer


torch.set_default_device("cuda")

transcriptions = glob.glob(os.path.join("./transcripts", "*.txt"))
device = "cuda"  # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2", load_in_4bit=True
)

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")


def summarize_text(text: str) -> str:
    messages = [
        {
            "role": "user",
            "content": "Summarize the following article in Russian in a maximum of 2 bullet points. Output in Russian language: `"
            + text
            + "`",
        },
    ]

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

    generated_ids = model.generate(encodeds, max_new_tokens=1000, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)

    summary = decoded[0].split("[/INST]")[-1].replace("</s>", "").strip()

    return summary


for transcription in transcriptions:
    print("transcribing", transcription)
    with open(transcription, "r") as file:
        text = file.read().replace('"', "")

    date = transcription.split("/")[-1].replace(".txt", "")
    summary = summarize_text(text)

    # write this to file with template
    # ----
    # title: [title]
    # description: [description]
    # ----
    #
    # [text]

    with open(f"./website/src/content/declaraciones/{date}.md", "w") as file:
        file.write(
            f"---\ntitle: Декларация от {date}\ndescription: {summary}\n---\n\n{text}"
        )


# # save segments to json fi
