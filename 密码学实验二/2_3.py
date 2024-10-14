import os
import random
from Crypto.Cipher import AES
import base64

def generate_random_aes_key():
    return os.urandom(16)

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pkcs7_pad(text, block_size):
    padding_len = block_size - (len(text) % block_size)
    padding = bytes([padding_len] * padding_len)
    return text + padding

def pkcs7_unpad(padded_text):
    padding_len = padded_text[-1]
    return padded_text[:-padding_len]

def ecb_encrypt(plain_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plain_text)

def ecb_decrypt(cipher_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(cipher_text)

def cbc_encrypt(plain_text, key, iv):
    block_size = len(key)
    plain_text = pkcs7_pad(plain_text, block_size)
    cipher_text = b''
    previous_block = iv

    for i in range(0, len(plain_text), block_size):
        block = plain_text[i:i + block_size]
        block = xor_bytes(block, previous_block)
        encrypted_block = ecb_encrypt(block, key)
        cipher_text += encrypted_block
        previous_block = encrypted_block

    return cipher_text

def cbc_decrypt(cipher_text, key, iv):
    block_size = len(key)
    plain_text = b''
    previous_block = iv

    for i in range(0, len(cipher_text), block_size):
        block = cipher_text[i:i + block_size]
        decrypted_block = ecb_decrypt(block, key)
        decrypted_block = xor_bytes(decrypted_block, previous_block)
        plain_text += decrypted_block
        previous_block = block

    return pkcs7_unpad(plain_text)

def encryption_oracle(input_data):
    key = generate_random_aes_key()
    prepend = os.urandom(random.randint(5, 10))
    append = os.urandom(random.randint(5, 10))
    plain_text = prepend + input_data + append

    if random.randint(0, 1) == 0:# 使用ECB模式
        cipher = AES.new(key, AES.MODE_ECB)
        padded_text = pkcs7_pad(plain_text, AES.block_size)
        encrypted = cipher.encrypt(padded_text)
        mode = "ECB"
    else:# 使用CBC模式
        iv = os.urandom(AES.block_size)
        encrypted = cbc_encrypt(plain_text, key, iv)
        mode = "CBC"
    return encrypted, mode

def detect_encryption_mode(encrypted_data):
    block_size = AES.block_size
    blocks = [encrypted_data[i:i + block_size] for i in range(0, len(encrypted_data), block_size)]
    if len(set(blocks)) != len(blocks):
        return "ECB"
    else:
        return "CBC"

if __name__ == "__main__":
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * 16 * 3
    plain_text = b"\xFF" * 16 * 3
    encrypted, mode = encryption_oracle(plain_text)
    detected_mode = detect_encryption_mode(encrypted)
    print(f"Actual mode: {mode}")
    print(f"Detected mode: {detected_mode}")