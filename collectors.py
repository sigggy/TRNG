import hashlib
import os
from defines import *

def collect_system_entropy():
    return os.urandom(DEV_RANDOM_BYTE_RETURN)

def collect_audio_entropy(stream):
    frames = []
    # Record audio in chunks
    for _ in range(0, int(16000 / 1024 * 1)):
        data = stream.read(1024)
        frames.append(data)
        
    raw_audio = b''.join(frames)
    return hashlib.sha256(raw_audio).digest()

def collect_video_entropy(cap):
    # Grab frame
    ret, frame = cap.read()
    # Grab the pixel values
    pixels = frame.flatten()
    # Hash down to 256 
    hashed = hashlib.sha256(pixels).digest()
    # return our hashed vals
    return hashed

def collect_all_entropy(cap, stream) -> bytes:
    sys_entropy = collect_system_entropy()
    audio_entropy = collect_audio_entropy(stream)
    video_entropy = collect_video_entropy(cap)
    

    # XOR all three sources together
    result = bytearray(COLLECT_ALL_RETURN_SIZE)
    for i in range(COLLECT_ALL_RETURN_SIZE):
        result[i] = sys_entropy[i] ^ audio_entropy[i] ^ video_entropy[i]
    
    return bytes(result)
