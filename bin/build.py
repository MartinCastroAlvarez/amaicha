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
    clip: editor.VideoFileClip = clip.subclip(0, 2)
    if len(clips) > 2: break

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
    clip: editor.VideoFileClip = vfx.speedx(clip, factor=0.95)

    # -------------------------------------------------------------
    # CLIP COLORS
    # Updating the colors of the Clip using OpenCV.
    # https://stackoverflow.com/questions/41596381
    # -------------------------------------------------------------
    for frames in clip.iter_frames():
        gray_frames = cv2.cvtColor(frames, cv2.COLOR_RGB2GRAY)
        # print(gray_frames)
        # TODO
        # TODO
        # TODO
        # TODO
        # TODO
    # raise Exception(123)

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
    factor: float = 10.3 * volume + 0.0997 / volume +  0.41
    clip: editor.VideoFileClip = afx.volumex(clip, factor=factor)

    # -------------------------------------------------------------
    # NEXT CLIP
    # Appending each Clip to the list of Clips.
    # -------------------------------------------------------------
    clips.append(clip)

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
for filename in sorted(glob.iglob("**.jpeg")):

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
    if len(clips) > 5: break

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
    clips.insert(0, clip)

# -------------------------------------------------------------
# CLIPS MERGE
# Conctenating all clips into a single long video.
# -------------------------------------------------------------
final: editor.VideoFileClip = editor.concatenate_videoclips(clips,
                                                            method="compose",
                                                            bg_color=(40, 40, 40))
print(f'All video clips: {final}')

# -------------------------------------------------------------
# TEXT CLIP
# Adding title text to the movie clips.
# -------------------------------------------------------------
# text: editor.TextClip = editor.TextClip("Feliz Cumple!")
# text: editor.TextClip = text.set_position('center')
# text: editor.TextClip = text.set_duration(final.duration)
# print(f'Text Clip: {text_clip}')
# final: editor.CompositeVideoClip([final, text])
# print(f'Final Clip: {final}')

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
audio: editor.AudioFileClip = afx.volumex(audio, factor=0.4)

# -------------------------------------------------------------
# AUDIO VIDEO
# Concatenating audio and video clips.
# -------------------------------------------------------------
audio: editor.AudioFileClip = audio.set_duration(final.duration)
final: editor.VideoFileClip = final.set_audio(editor.CompositeAudioClip([final.audio, audio]))
print(f'Audio File: {audio}')

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
