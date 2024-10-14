from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import re

KEY = get_random_bytes(16)
IV = get_random_bytes(16)

def pad(data):
    block_size = 16
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)

def unpad(data):
    padding = data[-1]
    return data[:-padding]

def sanitize_input(userdata):
    return re.sub(r'[;=]', lambda x: f"%{ord(x.group(0)):02x}", userdata)#将字符转换为16进制

def encrypt(userdata):
    prefix = b"comment1=cooking%20MCs;userdata="
    suffix = b";comment2=%20like%20a%20pound%20of%20bacon"
    sanitized_userdata = sanitize_input(userdata.decode()).encode()
    plaintext = prefix + sanitized_userdata + suffix
    padded_plaintext = pad(plaintext)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ciphertext = cipher.encrypt(padded_plaintext)
    print(f"Plaintext: {plaintext}")
    return ciphertext

def decrypt(ciphertext):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(ciphertext)
    unpadded_decrypted = unpad(decrypted)
    print(f"Decrypted: {unpadded_decrypted}")
    return b";admin=true;" in unpadded_decrypted

def bitflipping_attack():
    # 生成初始的密文
    userdata = b"A" * 16
    ciphertext = encrypt(userdata)
    print(f"Ciphertext: {ciphertext}")

    # 修改密文以注入 ";admin=true;"
    block_size = 16
    modified_ciphertext = bytearray(ciphertext)
    target = b";admin=true;"

    for i in range(len(target)):
        modified_ciphertext[block_size + i] ^= ord('A') ^ target[i]

    # 检查修改后的密文是否包含 ";admin=true;"
    return decrypt(bytes(modified_ciphertext))

if __name__ == "__main__":
    print("Bitflipping attack successful:", bitflipping_attack())