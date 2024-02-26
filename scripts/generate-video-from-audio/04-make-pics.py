import torch
import json

from diffusers import StableDiffusionPipeline


# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)


# load pipeline
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

for i, segment in enumerate(segments):
    image = pipe(segment["summarized"] + "| art painting").images[0]

    image.save("./data/" + str(i) + ".png")
