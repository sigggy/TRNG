import cv2
import subprocess
import random

def collect_system_entropy():
    return b'SYSTEM_ENTROPY_PLACEHOLDER'

def collect_audio_entropy():
    return b'AUDIO_ENTROPY_PLACEHOLDER'

def collect_video_entropy():
    # Grab url and commands to grab the stream
    url = "https://www.youtube.com/watch?v=DHUnz4dyb54"
    cmd = ['yt-dlp', '-g', url]

    try:
        # Get the stream
        stream_url = subprocess.check_output(cmd).decode().strip()
    except subprocess.CalledProcessError:
        print("Failed to retrieve stream URL.")
        return None
    
    # Feed it to CV2 
    cap = cv2.VideoCapture(stream_url)
    # Byte array to hold output
    entropy_bytes = bytearray()
    # Grab 10 frames
    for _ in range(10):
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Flatten that sucker down
        pixels = frame.flatten()
        # 100 pixel sample fo each frame
        sampled = random.sample(list(pixels), 100)
        # Add them to our byte array
        entropy_bytes.extend(sampled)
    # Release stream URL
    cap.release()
    return entropy_bytes

def collect_all_entropy():
    return (
        collect_system_entropy() +
        collect_audio_entropy() +
        collect_video_entropy()
    )