"""
RENDER
This script is responsible for rendering the web app.
"""

import os
import glob
import typing

import cv2
import numpy as np

from moviepy import editor
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

# ROOT DIRECTORY
# This is the root directory of the application.
ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f'Root directory: {ROOT}')

# MEDIA DIRECTORY
# This directory is used to read video sources.
MEDIA: str = os.path.join(ROOT, "media")
print(f'Media directory: {MEDIA}')
if not os.path.isdir(MEDIA):
    os.mkdir(MEDIA)

# RENDER DIRECTORY
# This directory is used to store the final result.
RENDER: str = os.path.join(ROOT, "render")
print(f'Render directory: {RENDER}')
if not os.path.isdir(RENDER):
    os.mkdir(RENDER)

# MOVIE CLIPS
# Iterating over each of the Clips on the MEDIA directory.
clips: typing.List[editor.VideoFileClip] = []
os.chdir(MEDIA)
for filename in sorted(glob.iglob("**.mp4")):

    # LOADING CLIP
    # Loading each subclip using MoviePy.
    # print(f'Video File: {filename}')
    clip: editor.VideoFileClip = editor.VideoFileClip(filename)

    # CLIP ROTATION
    # Rotating videos from sources such as WhatsApp that rotates videos.
    # These statements restore the proper rotation so that Clips can be merged.
    if clip.rotation in (90, 270):
        clip: editor.VideoFileClip = clip.resize(clip.size[::-1])
        clip.rotation = 0

    # SAMPLING
    # Cutting video during development.
    clip: editor.VideoFileClip = clip.subclip(0, 9)  # NOTE: Uncomment for sampling.
    if len(clips) > 3:                               # NOTE: Uncomment for sampling.
        break                                        # NOTE: Uncomment for sampling.

    # CLIP TRANSFORMATIONS
    # Applying different video effects and styling to all Clips.
    clip: editor.VideoFileClip = vfx.fadein(clip, duration=0.5)
    clip: editor.VideoFileClip = vfx.fadeout(clip, duration=0.5)
    clip: editor.VideoFileClip = vfx.lum_contrast(clip, contrast=0)
    clip: editor.VideoFileClip = vfx.lum_contrast(clip, lum=0.5)
    clip: editor.VideoFileClip = vfx.speedx(clip, factor=0.90)
    # clip: editor.VideoFileClip = vfx.supersample(clip, d=0.1, nframes=1)

    # CLIP MARGIN
    # Adding margin to this clip.
    # https://zulko.github.io/moviepy/examples/ukulele_concerto.html
    margin( 6,color=(255,255,255)).  #white margin
    margin( bottom=20, right=20, opacity=0). # transparent

    # CLIP AUDIO
    # Detecting the audio volumeX factor dynamically.
    # https://stackoverflow.com/questions/28119082
    # https://stackoverflow.com/questions/9012761
    #
    # The curve has been fit with this tool:
    # http://www.colby.edu/chemistry/PChem/scripts/lsfitpl.html
    sound: np.array = clip.audio.to_soundarray(fps=22000)
    sound: np.array = sound[sound > 0]
    sound.sort()
    PERCENTILE: float = 0.1
    low: int = int(PERCENTILE * sound.shape[0])
    high: int = int((1 - PERCENTILE) * sound.shape[0])
    volume: float = np.average(sound[low:high])
    factor: float = 10.3 * volume + 0.0997 / volume +  0.41
    clip: editor.VideoFileClip = afx.volumex(clip, factor=factor)

    # NEXT CLIP
    # Appending each Clip to the list of Clips.
    clips.append(clip)

# CLIPS MERGE
# Conctenating all clips into a single long video.
final: editor.VideoFileClip = editor.concatenate_videoclips(clips, method="compose")
print(f'All video clips: {final}')

# TEXT CLIP
# Adding title text to the movie clips.
# text: editor.TextClip = editor.TextClip("Feliz Cumple!")
# text: editor.TextClip = text.set_position('center')
# text: editor.TextClip = text.set_duration(final.duration)
# print(f'Text Clip: {text_clip}')
# final: editor.CompositeVideoClip([final, text])
# print(f'Final Clip: {final}')

# AUDIO CLIP
# Loading audio clip using MoviePy.
# https://stackoverflow.com/questions/55032551/moviepy-add-audio-to-a-video
# https://zulko.github.io/moviepy/getting_started/audioclips.html
os.chdir(MEDIA)
filename: str = [
    audio
    for audio in glob.iglob("**.mp3")
    if "TEMP" not in audio
][0]
audio: editor.AudioFileClip = editor.AudioFileClip(filename)
audio: editor.AudioFileClip = afx.volumex(audio, factor=0.4)

# AUDIO VIDEO
# Concatenating audio and video clips.
audio: editor.AudioFileClip = audio.set_duration(final.duration)
final: editor.VideoFileClip = final.set_audio(editor.CompositeAudioClip([final.audio, audio]))
print(f'Audio File: {audio}')

# GLOBAL TRANSFORMATIONS
# Applying transformations to the video after everything has been merged.
final: editor.VideoFileClip = afx.volumex(final, factor=0.8)

# RENDERING
# Storing the final clip into the RENDER directory.
path: str = os.path.join(RENDER, "final.mp4")
final.write_videofile(path, fps=23.98)
