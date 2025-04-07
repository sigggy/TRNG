import hashlib
import os
from audio_entropy import *
from defines import *

def collect_system_entropy():
    return os.urandom(DEV_RANDOM_BYTE_RETURN)

def collect_audio_entropy():
    return collect_audio(1)

def collect_video_entropy(cap):
    # Grab frame
    ret, frame = cap.read()
    # Grab the pixel values
    pixels = frame.flatten()
    # Hash down to 256 
    hashed = hashlib.sha256(pixels).digest()
    # return our hashed vals
    return hashed

def collect_all_entropy(cap) -> bytes:
    sys_entropy = collect_system_entropy()
    audio_entropy = collect_audio_entropy()
    video_entropy = collect_video_entropy(cap)
    

    # XOR all three sources together
    result = bytearray(COLLECT_ALL_RETURN_SIZE)
    for i in range(COLLECT_ALL_RETURN_SIZE):
        result[i] = sys_entropy[i] ^ audio_entropy[i] ^ video_entropy[i]
    
    return bytes(result)
