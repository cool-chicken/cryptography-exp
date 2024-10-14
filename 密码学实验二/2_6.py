import os
import random
from random import randint
import base64
from Crypto.Cipher import AES
from Crypto.Util import Padding

key = os.urandom(16)
prefix = os.urandom(randint(1, 15))
target = base64.b64decode(
            "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
            "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
            "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
            "YnkK"
        )
def encrypt(message):
    plaintext = Padding.pad(prefix + message + target, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plaintext)


# Finding the block size
previous_length = len(encrypt(b''))
for i in range(20):
    length = len(encrypt(b'X' * i))
    if length != previous_length:
        block_size = length - previous_length
        size_prefix_plus_target_aligned = previous_length
        min_known_ptxt_size_to_align = i
        break
else:
    raise Exception('did not detect any change in ciphertext length')

assert block_size == 16

# Finding the prefix size
def split_bytes_in_blocks(data, block_size):
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]

previous_blocks = None
for i in range(1, block_size + 1):
    blocks = split_bytes_in_blocks(encrypt(b'X' * i), block_size)
    if previous_blocks is not None and blocks[0] == previous_blocks[0]:
        prefix_size = block_size - i + 1
        break
    previous_blocks = blocks
else:
    raise Exception('did not detect constant ciphertext block')

assert prefix_size == len(prefix)

# Compute the size of the target
target_size = size_prefix_plus_target_aligned - min_known_ptxt_size_to_align - prefix_size
assert target_size == len(target)

# Decrypt the target bytes
known_target_bytes = b""
for _ in range(target_size):
    r = prefix_size
    k = len(known_target_bytes)
    padding_length = (-k - 1 - r) % block_size
    padding = b"X" * padding_length

    target_block_number = (k + r) // block_size
    target_slice = slice(target_block_number * block_size, (target_block_number + 1) * block_size)
    target_block = encrypt(padding)[target_slice]

    for i in range(256):
        message = padding + known_target_bytes + bytes([i])
        block = encrypt(message)[target_slice]
        if block == target_block:
            known_target_bytes += bytes([i])
            break

print(known_target_bytes.decode())