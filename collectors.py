import hashlib
import os

def collect_system_entropy():
    return os.urandom(256)

def collect_audio_entropy():
    return b'AUDIO_ENTROPY_PLACEHOLDER'

def collect_video_entropy(cap):
    # Grab frame
    ret, frame = cap.read()
    # Grab the pixel values
    pixels = frame.flatten()
    # Hash down to 256 
    hashed = hashlib.sha256(pixels).digest()
    # return our hashed vals
    return hashed

def collect_all_entropy(cap):
    return (
        collect_system_entropy() +
        collect_audio_entropy() +
        collect_video_entropy(cap)
    )