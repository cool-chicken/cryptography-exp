import hashlib
import base64
from Crypto.Cipher import AES
import binascii

def pad(text):
    padding_len = AES.block_size - len(text) % AES.block_size
    padding = b'\x01' + b'\x00' * (padding_len - 1)
    return text + padding

def unpad(text):
    return text.rstrip(b'\x00').rstrip(b'\x01')

def unknown_number():
    number = "111116"
    weight = "731"
    total = sum(int(number[i]) * int(weight[i % 3]) for i in range(len(number)))
    return total % 10

def calculate_kseed():
    MRZ_information = "12345678<8<<<1110182<1111167<<<<<<<<<<<<<<<4"
    H_information = hashlib.sha1((MRZ_information[:10] + MRZ_information[13:20] + MRZ_information[21:28]).encode()).hexdigest()
    return H_information[:32]

def calculate_ka_kb(K_seed):
    d = K_seed + "00000001"
    H_d = hashlib.sha1(binascii.unhexlify(d)).hexdigest()
    return H_d[:16], H_d[16:32]

def parity_check(hex_str):
    binary_str = bin(int(hex_str, 16))[2:].zfill(64)
    k_list = [(byte := binary_str[i:i + 7]) + ('1' if byte.count('1') % 2 == 0 else '0') for i in range(0, len(binary_str), 8)]
    return hex(int(''.join(k_list), 2))[2:].zfill(16)

def decrypt_message(encrypted_text):
    K_seed = calculate_kseed()
    ka, kb = calculate_ka_kb(K_seed)
    key = parity_check(ka) + parity_check(kb)
    print(f"Key: {key}")

    ciphertext = base64.b64decode(encrypted_text)
    IV = '0' * 32

    cipher = AES.new(binascii.unhexlify(key), AES.MODE_CBC, binascii.unhexlify(IV))
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted_message = unpad(decrypted_padded).decode('utf-8', errors='ignore')

    print(f"Decrypted message: {decrypted_message}")

if __name__ == "__main__":
    print(unknown_number())
    encrypted_text = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
    decrypt_message(encrypted_text)