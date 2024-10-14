import codecs

def decrypt_single_byte_xor(cipher_hex):
    cipher_bytes = codecs.decode(cipher_hex, 'hex')
    def is_english(text):
        return text.isascii() and text.isprintable()
    def english_score(text):
        return sum(1 for char in text if char.isalpha())
    best_key = None
    best_score = -1
    best_plaintext = ""
    
    for key in range(256):
        decrypted = bytes([cipher_bytes[i] ^ key for i in range(len(cipher_bytes))])
        decrypted_text = decrypted.decode('utf-8', errors='ignore')
        if is_english(decrypted_text):
            score = english_score(decrypted_text)
            if score > best_score:
                best_score = score
                best_key = key
                best_plaintext = decrypted_text
    return best_plaintext, best_key

cipher_hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
decrypted_text, key = decrypt_single_byte_xor(cipher_hex)
print("Decrypted Text:", decrypted_text)
print("Key:", hex(key))

# Output:
# Decrypted Text: Cooking MC's like a pound of bacon
# Key: 0x58