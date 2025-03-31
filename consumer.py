import time
from bank import read_from_bank
from defines import CHUNK_SIZE, CONSUMER_SLEEP_TIME

def consumer_loop():
    try:
        while True:
            data = read_from_bank(CHUNK_SIZE)
            if data:
                print(f"[CONSUMER] Read {CHUNK_SIZE} bytes: {data.hex()}")
            else:
                print("[CONSUMER] Not enough data to consume.")
            time.sleep(CONSUMER_SLEEP_TIME)

    except KeyboardInterrupt:
        print("\n[CONSUMER] KeyboardInterrupt received. Exiting gracefully.")
        print("[CONSUMER] Shutdown complete.")

if __name__ == "__main__":
    consumer_loop()
