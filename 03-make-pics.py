import torch
import json

from diffusers import StableDiffusionPipeline


# read data/segments.json
with open("data/segments.json", "r") as f:
    segments = json.load(f)

model_id = "dreamlike-art/dreamlike-anime-1.0"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

negative_prompt = 'simple background, duplicate, retro style, low quality, lowest quality, 1980s, 1990s, 2000s, 2005 2006 2007 2008 2009 2010 2011 2012 2013, bad anatomy, bad proportions, extra digits, lowres, username, artist name, error, duplicate, watermark, signature, text, extra digit, fewer digits, worst quality, jpeg artifacts, blurry'

for i, segment in enumerate(segments):
    image = pipe(segment["translated_text"][0],
                 negative_prompt=negative_prompt).images[0]

    image.save("./data/"+str(i)+".png")
