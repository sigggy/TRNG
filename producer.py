from collectors import collect_all_entropy
from buffer import EntropyBuffer
from bank import write_to_bank
import cv2
import pyaudio

buffer = EntropyBuffer()
# * This read will need to be reworked as we grow to scale 
# * Will likely need to implement some sort of rotating chunk files 

# Grab the webcam video
cap = cv2.VideoCapture(0)

# grab audio
audio = pyaudio.PyAudio()

# Open the audio stream
stream = audio.open(
    format=pyaudio.paInt16,  # 16-bit audio format
    channels=1,             # Mono audio
    rate=16000,
    input=True,
    frames_per_buffer=1024,
    input_device_index=0  # Specify the device index
)

def producer_loop():
    try:
        while True:
            entropy = collect_all_entropy(cap, stream)
            buffer.add(entropy)

            if buffer.should_flush():
                mixed = buffer.flush()
                write_to_bank(mixed)
                print(f"[PRODUCER] Wrote {len(mixed)} bytes to bank")
            else:
                print(f'[PRODUCER] doesn\'t have enough bytes in the buffer to flush')

    except KeyboardInterrupt:
        print("\n[PRODUCER] KeyboardInterrupt received. Exiting gracefully.")
        if buffer.should_flush():
            mixed = buffer.flush()
            write_to_bank(mixed)
            print(f"[PRODUCER] Final flush of {len(mixed)} bytes.")
        audio.terminate()
        stream.stop_stream()
        stream.close()
        print("[PRODUCER] Shutdown complete.")

if __name__ == "__main__":
    producer_loop()
