import portalocker
from defines import BANK_PATH

def write_to_bank(data: bytes):
    with open(BANK_PATH, 'ab+') as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        f.write(data)
        f.flush()
        portalocker.unlock(f)

def read_from_bank(chunk_size: int) -> bytes:
    with open(BANK_PATH, 'rb+') as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        data = f.read()
        if len(data) < chunk_size:
            portalocker.unlock(f)
            return b''
        result = data[:chunk_size]
        remaining = data[chunk_size:]
        f.seek(0)
        f.truncate()
        f.write(remaining)
        f.flush()
        portalocker.unlock(f)
        return result