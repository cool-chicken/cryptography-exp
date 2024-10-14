import re
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def parse_kv(kv_string):
    return dict(pair.split('=') for pair in kv_string.split('&'))

def profile_for(email):
    email = re.sub(r'[&=]', '', email)
    profile = {
        'email': email,
        'uid': 10,
        'role': 'user'
    }
    return f"email={profile['email']}&uid={profile['uid']}&role={profile['role']}"

def pad(data):
    block_size = 16
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)

def unpad(data):
    padding = data[-1]
    return data[:-padding]

def generate_key():
    return get_random_bytes(16)

def encrypt_profile(profile, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_profile = pad(profile.encode())
    return cipher.encrypt(padded_profile)

def decrypt_profile(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(ciphertext))
    return decrypted.decode()

def create_admin_profile():
    key = generate_key()
    email1 = "foo@bar.com"
    email2 = "foo@bar.comadmin" + "\x0b" * 11  

    encrypted1 = encrypt_profile(profile_for(email1), key)
    encrypted2 = encrypt_profile(profile_for(email2), key)
    crafted_ciphertext = encrypted1[:32] + encrypted2[16:32]

    decrypted_profile = decrypt_profile(crafted_ciphertext, key)
    return parse_kv(decrypted_profile)

if __name__ == "__main__":
    print(parse_kv("foo=bar&baz=qux&zap=zazzle"))
    print(profile_for("foo@bar.com"))
    key = generate_key()
    encrypted = encrypt_profile(profile_for("foo@bar.com"), key)
    print('---------------------------------')
    print(decrypt_profile(encrypted, key))
    print(create_admin_profile())