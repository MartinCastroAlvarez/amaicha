"""
RENDER
This script is responsible for rendering the web app.
"""

import os
import glob
import shutil
import typing

import cv2
import numpy as np

from moviepy import editor
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

# -------------------------------------------------------------
# ROOT DIRECTORY
# This is the root directory of the application.
# -------------------------------------------------------------
ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f'Root directory: {ROOT}')

# -------------------------------------------------------------
# MEDIA DIRECTORY
# This directory is used to read video sources.
# -------------------------------------------------------------
MEDIA: str = os.path.join(ROOT, "media")
print(f'Media directory: {MEDIA}')
if not os.path.isdir(MEDIA):
    os.mkdir(MEDIA)

# -------------------------------------------------------------
# RENDER DIRECTORY
# This directory is used to store the final result.
# -------------------------------------------------------------
RENDER: str = os.path.join(ROOT, "render")
print(f'Render directory: {RENDER}')
if not os.path.isdir(RENDER):
    os.mkdir(RENDER)

# -------------------------------------------------------------
# CLIPS
# Creating a list where individual Clips will be stored.
# -------------------------------------------------------------
clips: typing.List[editor.VideoFileClip] = []
names: typing.List[str] = []

# -------------------------------------------------------------
# MOVIE CLIPS
# Iterating over each of the Clips on the MEDIA directory.
# -------------------------------------------------------------
os.chdir(MEDIA)
for filename in sorted(glob.iglob("**.mp4")):

    # -------------------------------------------------------------
    # LOADING CLIP
    # Loading each subclip using MoviePy.
    # -------------------------------------------------------------
    clip: editor.VideoFileClip = editor.VideoFileClip(filename)
    print(f"Video clip: '{filename}'.")

    # -------------------------------------------------------------
    # CLIP ROTATION
    # Rotating videos from sources such as WhatsApp that rotates videos.
    # These statements restore the proper rotation so that Clips can be merged.
    # -------------------------------------------------------------
    if clip.rotation in (90, 270):
        clip: editor.VideoFileClip = clip.resize(clip.size[::-1])
        clip.rotation = 0

    # -------------------------------------------------------------
    # SAMPLING
    # Uncomment this code for sampling.
    # -------------------------------------------------------------
    # clip: editor.VideoFileClip = clip.subclip(0, 4)
    # if len(clips) > 4: break

    # -------------------------------------------------------------
    # CLIP MARGIN
    # Adding margin to this clip.
    # https://zulko.github.io/moviepy/examples/ukulele_concerto.html
    # -------------------------------------------------------------
    clip: editor.VideoFileClip = vfx.margin(clip, mar=20, color=(245, 248, 250))

    # -------------------------------------------------------------
    # CLIP TRANSFORMATIONS
    # Applying different video effects and styling to all Clips.
    # -------------------------------------------------------------
    clip: editor.VideoFileClip = vfx.fadein(clip, duration=1)
    clip: editor.VideoFileClip = vfx.fadeout(clip, duration=1)
    clip: editor.VideoFileClip = vfx.lum_contrast(clip, contrast=0.2, lum=3)
    # clip: editor.VideoFileClip = vfx.speedx(clip, factor=0.90)

    # -------------------------------------------------------------
    # CLIP AUDIO
    # Detecting the audio volumeX factor dynamically.
    # https://stackoverflow.com/questions/28119082
    # https://stackoverflow.com/questions/9012761
    # The curve has been fit with this tool:
    # http://www.colby.edu/chemistry/PChem/scripts/lsfitpl.html
    # -------------------------------------------------------------
    sound: np.array = clip.audio.to_soundarray(fps=22000)
    sound: np.array = sound[sound > 0]
    sound.sort()
    PERCENTILE: float = 0.1
    low: int = int(PERCENTILE * sound.shape[0])
    high: int = int((1 - PERCENTILE) * sound.shape[0])
    volume: float = np.average(sound[low:high])
    factor: float = max(0.1, 10.3 * volume + 0.1597 / volume - 0.41)
    clip: editor.VideoFileClip = afx.volumex(clip, factor=factor)

    # -------------------------------------------------------------
    # NEXT CLIP
    # Appending each Clip to the list of Clips.
    # -------------------------------------------------------------
    clips.append(clip)
    names.append(filename)

# -------------------------------------------------------------
# VIDEO RESIZING
# Calculating the maximum height and width of videos
# so that images can't be large than them.
# -------------------------------------------------------------
max_width: int = max(clip.size[0] for clip in clips)
max_height: int = max(clip.size[0] for clip in clips)

# -------------------------------------------------------------
# IMAGE CLIPS
# Iterating over each of the Clips on the MEDIA directory.
# -------------------------------------------------------------
os.chdir(MEDIA)
for i, filename in enumerate(sorted(glob.iglob("**.jpeg"))):

    # -------------------------------------------------------------
    # LOADING CLIP
    # Loading each subclip using MoviePy.
    # -------------------------------------------------------------
    clip: editor.ImageClip = editor.ImageClip(filename)
    print(f"Image clip: '{filename}'.")

    # -------------------------------------------------------------
    # SAMPLING
    # Uncomment this code for sampling.
    # -------------------------------------------------------------
    # if len(clips) > 5: break

    # -------------------------------------------------------------
    # CLIP MARGIN
    # Adding margin to this clip.
    # https://zulko.github.io/moviepy/examples/ukulele_concerto.html
    # -------------------------------------------------------------
    clip: editor.ImageClip = vfx.margin(clip, mar=20, color=(245, 248, 250))

    # -------------------------------------------------------------
    # CLIP DURATION
    # Setting the clip duration for each image.
    # -------------------------------------------------------------
    clip: editor.ImageClip = clip.set_duration(5)

    # -------------------------------------------------------------
    # CLIP TRANSFORMATIONS
    # Applying different video effects and styling to all Clips.
    # -------------------------------------------------------------
    clip: editor.ImageClip = vfx.fadein(clip, duration=1)
    clip: editor.ImageClip = vfx.fadeout(clip, duration=1)
    clip: editor.ImageClip = vfx.lum_contrast(clip, contrast=0.2, lum=3)

    # -------------------------------------------------------------
    # RESIZING VIDEO
    # https://zulko.github.io/moviepy/ref/videofx/moviepy.video.fx.all.resize.html
    # -------------------------------------------------------------
    if clip.size[0] > max_width:
        clip: editor.ImageClip = vfx.resize(clip, width=max_width)
    if clip.size[1] > max_height:
        clip: editor.ImageClip = vfx.resize(clip, height=max_height)

    # -------------------------------------------------------------
    # NEXT CLIP
    # Appending each Clip to the list of Clips.
    # -------------------------------------------------------------
    clips.insert(i, clip)
    names.insert(i, filename)

# -------------------------------------------------------------
# CLIPS MERGE
# Conctenating all clips into a single long video.
# -------------------------------------------------------------
final: editor.VideoFileClip = editor.concatenate_videoclips(clips,
                                                            method="compose",
                                                            bg_color=(0, 0, 0))
print(f'All video clips: {names}')

# -------------------------------------------------------------
# TEXT CLIP
# Adding title text to the movie clips.
# https://www.geeksforgeeks.org/moviepy-creating-text-clip/
# -------------------------------------------------------------
# text: editor.TextClip = editor.TextClip("Feliz Cumple!",
#                                         font="Arial-Bold",
#                                         fontsize=70,
#                                         color="white")
# text: editor.TextClip = text.set_position(('center', 'bottom'))
# text: editor.TextClip = text.set_duration(final.duration)
# print(f'Text clip: {text}')
# final: editor.CompositeVideoClip([final, text])
# print(f'Final clip: {final}')

# -------------------------------------------------------------
# AUDIO CLIP
# Loading audio clip using MoviePy.
# https://stackoverflow.com/questions/55032551/moviepy-add-audio-to-a-video
# https://zulko.github.io/moviepy/getting_started/audioclips.html
# -------------------------------------------------------------
os.chdir(MEDIA)
filename: str = [
    audio
    for audio in glob.iglob("**.mp3")
    if "TEMP" not in audio
][0]
audio: editor.AudioFileClip = editor.AudioFileClip(filename)
audio: editor.AudioFileClip = afx.volumex(audio, factor=0.5)

# -------------------------------------------------------------
# AUDIO TRANSFORMATIONS
# Applying different audio effects to the background audio.
# -------------------------------------------------------------
audio: editor.AudioFileClip = afx.audio_fadein(audio, duration=1)
audio: editor.AudioFileClip = afx.audio_fadeout(audio, duration=1)

# -------------------------------------------------------------
# AUDIO LOOP
# Creating an infinite loop of the audio so that it is enough
# to cover the video.
# TODO: In future versions, multiple audios should be supported.
# -------------------------------------------------------------
audio: editor.AudioFileClip = afx.audio_loop(audio, nloops=100)

# -------------------------------------------------------------
# AUDIO VIDEO
# Concatenating audio and video clips.
# -------------------------------------------------------------
if final.audio.duration > audio.duration:
    raise RuntimeError("Video is longer than the Audio:", final.audio.duration, audio.duration)
final: editor.AudioFileClip = final.set_duration(int(final.duration))
audio: editor.AudioFileClip = audio.set_duration(int(final.duration))
final: editor.VideoFileClip = final.set_audio(editor.CompositeAudioClip([final.audio, audio]))
print(f'Audio File: {audio}')
if final.audio.duration != audio.duration:
    raise RuntimeError("Video and Audio are out of sync:", final.audio.duration, audio.duration)

# -------------------------------------------------------------
# GLOBAL TRANSFORMATIONS
# Applying transformations to the video after everything has been merged.
# -------------------------------------------------------------
final: editor.VideoFileClip = afx.volumex(final, factor=0.8)

# -------------------------------------------------------------
# RENDERING
# Storing the final clip into the RENDER directory.
# -------------------------------------------------------------
path: str = os.path.join(RENDER, "final.mp4")
tmp: str = os.path.join(RENDER, "final.tmp.mp4")
final.write_videofile(tmp, fps=23.98)
shutil.copy2(tmp, path)
os.remove(tmp)
