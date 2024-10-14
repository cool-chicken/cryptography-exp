from Crypto.Cipher import AES
import base64
import os

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pkcs7_unpad(padded_text):
    padding_len = padded_text[-1]
    return padded_text[:-padding_len]

def ecb_decrypt(cipher_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(cipher_text)

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

if __name__ == "__main__":
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * 16
    with open("2_2.txt",'r') as f:
        ciphertext = base64.b64decode(f.read())
    plain_text = cbc_decrypt(ciphertext, key, iv)
    print(f"plaintext: {plain_text.decode()}")