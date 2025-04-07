import pyaudio
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import hashlib
import binascii

def collect_audio(duration):
    """
    Collects audio entropy by recording audio from the default microphone and hashes it to a fixed 256-bit sequence.

    Args:
        duration (int): Duration of the recording in seconds.

    Returns:
        bytes: Raw audio data collected from the microphone.
    """

    # Collect audio data
    audio_data = record_audio(duration)

    # Compress the audio data to a 256-bit hash
    compressed_data = compress_to_256_bytes(audio_data)
    # print(compressed_data)

    return compressed_data

def record_audio(duration, sample_rate=44100, chunk_size=1024, amplification_factor=10):
    """
    Collects and amplifies audio entropy by recording audio from the default microphone.

    Args:
        duration (int): Duration of the recording in seconds.
        sample_rate (int): Sampling rate in Hz.
        chunk_size (int): Number of frames per buffer.
        amplification_factor (float): Factor by which to amplify the audio.

    Returns:
        bytes: Amplified raw audio data collected from the microphone.
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

    # print(f"[AUDIO] Recording {duration} second(s) of audio...")
    frames = []

    # Record audio in chunks
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # print("[AUDIO] Recording complete.")

    # Combine frames and amplify
    raw_audio = b''.join(frames)
    amplified_audio = amplify_audio(raw_audio, amplification_factor)

    return amplified_audio

def amplify_audio(data, amplification_factor):
    """
    Amplifies the raw audio data.

    Args:
        data (bytes): Raw audio data.
        amplification_factor (float): Factor by which to amplify the audio.

    Returns:
        bytes: Amplified audio data.
    """
    # Convert bytes to numpy array of 16-bit integers
    audio_array = np.frombuffer(data, dtype=np.int16)

    # Amplify the audio
    # amplified_audio = np.clip(audio_array * amplification_factor, -32768, 32767)

    # Convert back to bytes
    return audio_array.astype(np.int16).tobytes()

def compress_to_256_bytes(data):
    """
    Compresses the raw audio data to a fixed 256-bit (32-byte) sequence using SHA-256.

    Args:
        data (bytes): Raw audio data.

    Returns:
        bytes: A 256-bit (32-byte) sequence derived from the audio data.
    """
    # Use SHA-256 to hash the data
    hash_object = hashlib.sha256(data)
    return hash_object.digest()  # Return the 32-byte hash directly

def plot_frequency_spectrum(data, sample_rate):
    """
    Plots the frequency spectrum of the audio data.

    Args:
        data (bytes): Raw audio data.
        sample_rate (int): Sampling rate in Hz.
    """
    # Convert bytes to numpy array of 16-bit integers
    audio_array = np.frombuffer(data, dtype=np.int16)

    # Perform FFT
    N = len(audio_array)
    freq = np.fft.fftfreq(N, d=1/sample_rate)
    magnitude = np.abs(fft(audio_array))

    # Plot the spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(freq[:N // 2], magnitude[:N // 2])  # Plot only positive frequencies
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # # Example usage
    # audio_data = record_audio(duration=1, sample_rate=44100, amplification_factor=5)
    # print(f"[AUDIO] Collected {len(audio_data)} bytes of audio data.")
    
    # # Compress the audio data to a 256-bit hash
    # compressed_data = compress_to_256_bytes(audio_data)
    
    # # Convert the compressed data to a hexadecimal string
    # hex_representation = binascii.hexlify(compressed_data).decode('utf-8')
    # print(f"[AUDIO] Hexadecimal representation: {hex_representation}")

    # # Plot the frequency spectrum of the raw audio data
    # plot_frequency_spectrum(audio_data, sample_rate=16000)
    
    collect_audio(1)
