import torch
import json

from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel


# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)

# load pipeline
model_id = "stabilityai/stable-diffusion-xl-base-1.0"
pipe = StableDiffusionXLPipeline.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")

# load finetuned model
unet_id = "mhdang/dpo-sdxl-text2image-v1"
unet = UNet2DConditionModel.from_pretrained(unet_id, subfolder="unet", torch_dtype=torch.float16)
pipe.unet = unet
pipe = pipe.to("cuda")


for i, segment in enumerate(segments):
    image = pipe(segment["summarized"] + "| pixar, 3d render, detailed happy").images[0]

    image.save("./data/"+str(i)+".png")
