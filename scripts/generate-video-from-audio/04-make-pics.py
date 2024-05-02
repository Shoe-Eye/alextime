import torch
import json

from diffusers import StableDiffusionXLPipeline

seed = 42

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16
).to("cuda")

pipe.load_lora_weights(
    "/home/cwiz/code/ai/diffusers/examples/dreambooth/alextime",
    weight_name="pytorch_lora_weights.safetensors",
    adapter_name="alextime",
)
# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)

for i, segment in enumerate(segments):

    prompt = "Criminal movie poster about alextime `" + segment["summary"] + "`"

    image = pipe(
        prompt,
        num_inference_steps=60,
        guidance_scale=8.5,
    ).images[0]

    image.save("./data/" + str(i) + ".png")
