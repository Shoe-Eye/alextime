import json
import glob, os

from moviepy.editor import *


with open("data/segments.json", "r") as f:
    segments = json.load(f)

clips_ = list(
    sorted(
        glob.glob("./data/*.gif"),
        key=lambda filename: int(filename.split("/")[-1].split(".")[0]),
    )
)
print(clips_)

# create clips from images with specified durations
clips = []
for i, segment in enumerate(segments):
    start = float(segment["start"])
    try:
        clip = VideoFileClip(clips_[i]).set_start(start)
    except:
        continue
    if i < len(segments) - 1:
        end = float(segments[i + 1]["start"])
    else:
        end = float(segment["end"])
    clip = clip.set_end(end)
    clips.append(clip)

# concatenate clips into final video
final_clip = concatenate_videoclips(clips)
audio_clip = AudioFileClip("./calls/2024-04-04.m4a")
final_clip = final_clip.set_audio(audio_clip)

# write final video to file
final_clip.write_videofile("./data/video.mp4", fps=24)
