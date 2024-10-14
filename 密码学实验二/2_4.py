import base64
from Crypto import Random
from Crypto.Cipher import AES

UNKNOWN_STRING = base64.b64decode(
    b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    b"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    b"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
    b"YnkK"
)
KEY = Random.new().read(16)

def pad(data, block_size=16):
    padding_len = block_size - len(data) % block_size
    return data + bytes([padding_len] * padding_len)

def encryption_oracle(your_string):
    plaintext = pad(your_string + UNKNOWN_STRING)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(plaintext)

def detect_block_size():
    initial_len = len(encryption_oracle(b""))
    for i in range(1, 256):
        data = b"A" * i
        new_len = len(encryption_oracle(data))
        if new_len != initial_len:
            return new_len - initial_len

def detect_mode(cipher):
    block_size = 16
    blocks = [cipher[i:i + block_size] for i in range(0, len(cipher), block_size)]
    return "ECB" if len(blocks) > len(set(blocks)) else "not ECB"

def ecb_decrypt(block_size):
    known_bytes = b""
    while True:
        block_index = len(known_bytes) // block_size
        block_offset = block_size - 1 - (len(known_bytes) % block_size)
        prefix = b"A" * block_offset
        target_block = encryption_oracle(prefix)[: (block_index + 1) * block_size]

        found = False
        for i in range(256):
            guess = prefix + known_bytes + bytes([i])
            if encryption_oracle(guess)[: (block_index + 1) * block_size] == target_block:
                known_bytes += bytes([i])
                found = True
                break
        if not found:
            print(f"Decrypted text: {known_bytes.decode('ascii', errors='ignore')}")
            return

def main():
    block_size = detect_block_size()
    print(f"Detected block size: {block_size}")
    cipher = encryption_oracle(b"A" * 50)
    mode = detect_mode(cipher)
    print(f"Detected mode: {mode}")
    ecb_decrypt(block_size)

if __name__ == "__main__":
    main()