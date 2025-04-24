import hashlib
import os
from defines import *
import cv2
import numpy as np

def collect_system_entropy():
    return os.urandom(DEV_RANDOM_BYTE_RETURN)

def collect_audio_entropy(stream):
    frames = []
    # Record audio in chunks
    for _ in range(0, int(AUDIO_SAMPLE_RATE / AUDIO_CHUNK_SIZE * 1)):
        data = stream.read(AUDIO_CHUNK_SIZE)
        if not data or all(b == 0 for b in data):
            raise ValueError("Low audio entropy")
        frames.append(data)
        
    raw_audio = b''.join(frames)
    return hashlib.sha3_256(raw_audio).digest()

def collect_video_entropy(cap, min_entropy_threshold=0.1, max_retries = 5):
    
    for _ in range(max_retries):
        # Grab frame
        ret, frame = cap.read()
        # Convert frame to grayscale (reduces redundancy)
        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pixels = frame.flatten()

        # --- Error Checks ---
        # 1. Check for all zeros/ones
        if np.all(pixels == 0) or np.all(pixels == 255):
            print("Rejected frame: All zeros/ones!")
            continue

        # 2. Check for low Shannon entropy (measure of randomness)
        hist = np.histogram(pixels, bins=256, range=(0, 256))[0]
        prob = hist / hist.sum()
        shannon_entropy = -np.sum(prob * np.log2(prob + 1e-10))  # Add epsilon to avoid log(0)
        if shannon_entropy < min_entropy_threshold:
            print(f"Rejected frame: Low entropy ({shannon_entropy:.2f} < {min_entropy_threshold})")
            continue

        # 3. Check for frozen frames (compare to previous frame)
        if hasattr(collect_video_entropy, 'last_frame'):
            if np.array_equal(frame, collect_video_entropy.last_frame):
                print("Rejected frame: Frozen/duplicate!")
                continue
        collect_video_entropy.last_frame = frame  # Update last frame

        # --- Hash Validated Frame ---
        return hashlib.sha3_256(pixels).digest()
    print(f"Failed to get valid frame after {max_retries} retries. Using fallback entropy.")
    return os.urandom(32)

def collect_all_entropy(creek_cap, fishtank_cap, stream) -> bytes:
    sys_entropy = collect_system_entropy()
    audio_entropy = collect_audio_entropy(stream)
    #creek_entropy = collect_video_entropy(creek_cap)
    fishtank_entropy = collect_video_entropy(fishtank_cap)
    
    # XOR all three sources together
    result = bytearray(COLLECT_ALL_RETURN_SIZE)
    for i in range(COLLECT_ALL_RETURN_SIZE):
        result[i] = sys_entropy[i] ^ audio_entropy[i] ^ fishtank_entropy[i] #^ creek_entropy[i]
    
    return bytes(result)
