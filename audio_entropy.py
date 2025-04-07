import pyaudio

def collect_audio_entropy(duration=1, sample_rate=44100, chunk_size=1024):
    """
    Collects audio entropy by recording audio from the default microphone.

    Args:
        duration (int): Duration of the recording in seconds.
        sample_rate (int): Sampling rate in Hz.
        chunk_size (int): Number of frames per buffer.

    Returns:
        bytes: Raw audio data collected from the microphone.
    """
    audio = pyaudio.PyAudio()

    # Open the audio stream
    stream = audio.open(
        format=pyaudio.paInt16,  # 16-bit audio format
        channels=1,             # Mono audio
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size
    )

    print(f"[AUDIO] Recording {duration} second(s) of audio...")
    frames = []

    # Record audio in chunks
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("[AUDIO] Recording complete.")
    return b''.join(frames)

def playback_audio(data, sample_rate=44100, chunk_size=1024):
    """
    Plays back the recorded audio data.

    Args:
        data (bytes): Raw audio data to be played back.
        sample_rate (int): Sampling rate in Hz.
        chunk_size (int): Number of frames per buffer.
    """
    audio = pyaudio.PyAudio()

    # Open the audio stream for playback
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        output=True,
        frames_per_buffer=chunk_size
    )

    print("[AUDIO] Playing back recorded audio...")
    stream.write(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("[AUDIO] Playback complete.")

if __name__ == "__main__":
    # Example usage
    audio_data = collect_audio_entropy(duration=1)  # Record 1 second of audio
    print(f"[AUDIO] Collected {len(audio_data)} bytes of audio data.")
    # You can now use `audio_data` for further processing or entropy extraction.
    playback_audio(audio_data)  # Play back the recorded audio