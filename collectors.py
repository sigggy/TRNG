import cv2
import subprocess
import hashlib
import os

def collect_system_entropy():
    return os.urandom(256)

def collect_audio_entropy():
    return b'AUDIO_ENTROPY_PLACEHOLDER'

def collect_video_entropy():
    # Grab url and commands to grab the stream
    url = "https://www.youtube.com/watch?v=DHUnz4dyb54"
    cmd = ['yt-dlp', '-g', url]

    # Get the stream
    stream_url = subprocess.check_output(cmd).decode().strip()
    # Feed it to CV2 
    cap = cv2.VideoCapture(stream_url)

    # Grab frame
    ret, frame = cap.read()
    # Grab the pixel values
    pixels = frame.flatten()
    # Hash down to 256 
    hashed = hashlib.sha256(pixels).digest()
    # Release stream URL
    cap.release()

    # return our hashed vals
    return hashed

def collect_all_entropy():
    return (
        collect_system_entropy() +
        collect_audio_entropy() +
        collect_video_entropy()
    )