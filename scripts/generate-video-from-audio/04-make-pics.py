import torch
import json

from diffusers import (
    StableDiffusionXLPipeline,
    KDPM2AncestralDiscreteScheduler,
    AutoencoderKL,
)

# Load VAE component
vae = AutoencoderKL.from_pretrained(
    "madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16
)

# Configure the pipeline
pipe = StableDiffusionXLPipeline.from_pretrained(
    "dataautogpt3/ProteusV0.4", vae=vae, torch_dtype=torch.float16
)
pipe.scheduler = KDPM2AncestralDiscreteScheduler.from_config(pipe.scheduler.config)
pipe.to("cuda")


# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)


for i, segment in enumerate(segments):

    prompt = segment["summarized"] + "best quality, extremely detailed, cartoon"
    negative_prompt = "nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, blur, blurry, ugly, wrongs proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, deformed, noisy image"

    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        width=1024,
        height=1024,
        guidance_scale=4,
        num_inference_steps=20,
    ).images[0]

    image.save("./data/" + str(i) + ".png")
