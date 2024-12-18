def xor(plaintext, key):
    repeated_key = (key * (len(plaintext) // len(key))) + key[:len(plaintext) % len(key)]
    encrypted_decrypted = bytes([p ^ k for p, k in zip(plaintext.encode(), repeated_key.encode())])
    return encrypted_decrypted.hex()

plaintext = '''Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal'''
key = "ICE"
encrypted1 = xor(plaintext, key)
print("Encrypted:", encrypted1)

# Output:Encrypted: 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20690a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f