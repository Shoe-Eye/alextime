import json

from moviepy.editor import *


with open("data/segments.json", "r") as f:
    segments = json.load(f)

# create clips from images with specified durations
clips = []
for i, segment in enumerate(segments):
    clip = ImageClip(
        "./data/"+str(i)+".png").set_start(segment["start"]).set_end(segment["end"])
    clips.append(clip)

# concatenate clips into final video
final_clip = concatenate_videoclips(clips)
audio_clip = AudioFileClip("./data/audio.mp3")
final_clip = final_clip.set_audio(audio_clip)

# write final video to file
final_clip.write_videofile("./data/video.mp4", fps=24)
