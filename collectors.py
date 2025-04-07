import cv2
import subprocess
import hashlib
import os
import defines 

def collect_system_entropy():
    return os.urandom(DEV_RANDOM_BYTE_RETURN)

def collect_audio_entropy():
    return b'\x00' * 32

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

def collect_all_entropy() -> bytes:
    sys_entropy = collect_system_entropy()
    audio_entropy = collect_audio_entropy()
    video_entropy = collect_video_entropy()
    
    print(len(sys_entropy))
    print(len(audio_entropy))
    print(len(video_entropy))
    
    # XOR all three sources together
    result = bytearray(COLLECT_ALL_RETURN_SIZE)
    for i in range(COLLECT_ALL_RETURN_SIZE):
        result[i] = sys_entropy[i] ^ audio_entropy[i] ^ video_entropy[i]
    
    return bytes(result)