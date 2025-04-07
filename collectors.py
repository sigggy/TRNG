import os

def collect_system_entropy():
    return os.urandom(256)

def collect_audio_entropy():
    return b'AUDIO_ENTROPY_PLACEHOLDER'

def collect_video_entropy():
    return b'VIDEO_ENTROPY_PLACEHOLDER'

def collect_all_entropy() -> bytes:
    sys_entropy = collect_system_entropy()
    audio_entropy = collect_audio_entropy()
    video_entropy = collect_video_entropy()

    return bytes(
        s ^ a ^ v for s, a, v in zip(sys_entropy, audio_entropy, video_entropy)
    )