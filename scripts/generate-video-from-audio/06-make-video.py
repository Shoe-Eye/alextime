import json
import glob, os

from moviepy.editor import *


with open("data/segments.json", "r") as f:
    segments = json.load(f)

clips_ = list(sorted(glob.glob("./data/*.png")))
print(clips_)

# create clips from images with specified durations
clips = []
for i, segment in enumerate(segments):
    start = int(segment["start"])
    end = int(segment["end"])
    clip = ImageClip(clips_[i]).loop(duration=end - start).set_start(start).set_end(end)
    clips.append(clip)

# concatenate clips into final video
final_clip = concatenate_videoclips(clips)
audio_clip = AudioFileClip("./calls/2023-12-21.m4a")
final_clip = final_clip.set_audio(audio_clip)

# write final video to file
final_clip.write_videofile("./data/video.mp4", fps=24)
