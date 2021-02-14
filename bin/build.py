"""
RENDER
This script is responsible for rendering the web app.
"""

import os
import glob
import typing

import cv2
from moviepy import editor
import moviepy.video.fx.all as vfx

SAMPLE: int = 3  # TODO: Remove this.

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

# ENHANCED DIRECTORY
# This directory is used for intermediate results.
ENHANCED: str = os.path.join(ROOT, "enhanced")
print(f'Media directory: {ENHANCED}')
if not os.path.isdir(ENHANCED):
    os.mkdir(ENHANCED)

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
for filename in sorted(glob.iglob("**.mp4"))[:SAMPLE]:

    # LOADING CLIP
    # Loading each subclip using MoviePy.
    print(f'Video File: {filename}')
    clip: editor.VideoFileClip = editor.VideoFileClip(filename)

    # CLIP ROTATION
    # Rotating videos from sources such as WhatsApp that rotates videos.
    # These statements restore the proper rotation so that Clips can be merged.
    if clip.rotation in (90, 270):
        clip: editor.VideoFileClip = clip.resize(clip.size[::-1])
        clip.rotation = 0

    # CLIP TRANSFORMATIONS
    # Applying different effects and styling to all Clips.
    clip: editor.VideoFileClip = vfx.fadein(clip, duration=0.5)
    clip: editor.VideoFileClip = vfx.fadeout(clip, duration=0.5)
    clip: editor.VideoFileClip = vfx.lum_contrast(clip, contrast=0)
    clip: editor.VideoFileClip = vfx.lum_contrast(clip, lum=1)
    clip: editor.VideoFileClip = vfx.speedx(clip, factor=0.95)
    clip: editor.VideoFileClip = vfx.gamma_corr(clip, gamma=0)

    # ENHANCHED RESULT
    # Storing enhanced intermediate result into the ENHANCED directory.
    # path: str = os.path.join(ENHANCED, filename)
    # clip.write_videofile(path, fps=23.98)

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
filename: str = list(glob.iglob("**.mp3"))[0]
audio: editor.AudioFileClip = editor.AudioFileClip(filename)
audio: editor.AudioFileClip = audio.set_duration(final.duration)
final.set_audio(editor.CompositeAudioClip([final.audio, audio]))
print(f'Audio File: {audio}')

# RENDERING
# Storing the final clip into the RENDER directory.
path: str = os.path.join(RENDER, "final.mp4")
final.write_videofile(path, fps=23.98)
