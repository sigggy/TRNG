from pathlib import Path 
import hashlib


# ========== Entropy Collection ==========

def collect_system_entropy() -> bytes:
    data = b'SYSTEM_ENTROPY_PLACEHOLDER'
    append_to_file(Path('raw_bytes') / 'system_entropy.log', data)
    return data

def collect_audio_entropy() -> bytes:
    data = b'AUDIO_ENTROPY_PLACEHOLDER'
    append_to_file(Path('raw_bytes') / 'audio_entropy.log', data)
    return data

def collect_video_entropy() -> bytes:
    data = b'VIDEO_ENTROPY_PLACEHOLDER'
    append_to_file(Path('raw_bytes') / 'video_entropy.log', data)
    return data

def append_to_file(file_path: Path, data: bytes):
    file_path.parent.mkdir(parents=True, exist_ok=True) 
    with file_path.open('ab') as f:  
        f.write(data + b'\n')

# ========== Entropy Combination ==========

def mix_entropy(sources_list) -> bytes:
    PASS 


# ========== Output Generation ==========

def generate_random_bytes(length) -> bytes:
    output = b''
    counter = 0

    while len(output) < length:
        # Recollect entropy each round (or optionally reseed less frequently)
        system_entropy = collect_system_entropy()
        audio_entropy = collect_audio_entropy()
        video_entropy = collect_video_entropy()

        mixed = mix_entropy([
            system_entropy,
            audio_entropy,
            video_entropy,
            counter.to_bytes(4, 'big')
        ])

        output += mixed
        counter += 1

    return output[:length]

# ========== Main Driver (for testing/demo) ==========

def request_random_bytes(length, return_format):
    return generate_random_bytes(length)
 

if __name__ == "__main__":
    desired_length = 64  
    random_bytes = generate_random_bytes(desired_length)
    
    # Print in hex for readability
    print(f"Random Bytes ({desired_length}):\n{random_bytes.hex()}")
