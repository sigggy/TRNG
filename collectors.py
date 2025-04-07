import os

def collect_system_entropy():
    return os.urandom(256)

def collect_audio_entropy():
    return b'AUDIO_ENTROPY_PLACEHOLDER'

def collect_video_entropy():
    return b'VIDEO_ENTROPY_PLACEHOLDER'

def collect_all_entropy():
    return (
        collect_system_entropy() +
        collect_audio_entropy() +
        collect_video_entropy()
    )