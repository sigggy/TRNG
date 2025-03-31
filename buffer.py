import hashlib
from defines import FLUSH_THRESHOLD

class EntropyBuffer:
    def __init__(self):
        self.buffer = bytearray()

    def add(self, data: bytes):
        self.buffer.extend(data)

    def should_flush(self):
        return len(self.buffer) >= FLUSH_THRESHOLD

    def flush(self) -> bytes:
        if not self.buffer:
            return b''
        digest = hashlib.sha256(self.buffer).digest()
        self.buffer.clear()
        return digest
