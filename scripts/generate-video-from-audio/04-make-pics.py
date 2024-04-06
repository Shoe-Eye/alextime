import torch
import json

from diffusers import StableDiffusionPipeline, AutoencoderKL

repo = "IDKiro/sdxs-512-0.9"
seed = 42
weight_type = torch.float32  # or float16

pipe = StableDiffusionPipeline.from_pretrained(repo, torch_dtype=weight_type)
pipe.to("cuda")


# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)


for i, segment in enumerate(segments):

    prompt = segment["summarized"] + ", photograph, moody light, golden hour"
    negative_prompt = "nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, blur, blurry, ugly, wrongs proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, deformed, noisy image"

    image = pipe(
        prompt,
        num_inference_steps=1,
        guidance_scale=0,
        generator=torch.Generator(device="cuda").manual_seed(seed),
    ).images[0]

    image.save("./data/" + str(i) + ".png")
