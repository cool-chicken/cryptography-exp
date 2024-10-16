def get_english_score(input_bytes):
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in input_bytes.lower()])

def single_char_xor(input_bytes, char_value):
    output_bytes = b''
    for byte in input_bytes:
        output_bytes += bytes([byte ^ char_value])
    return output_bytes

def bruteforce_single_char_xor(ciphertext):
    potential_messages = []
    for key_value in range(256):
        message = single_char_xor(ciphertext, key_value)
        score = get_english_score(message)
        data = {
            'message': message,
            'score': score,
            'key': key_value
        }
        potential_messages.append(data)
    return sorted(potential_messages, key=lambda x: x['score'], reverse=True)[0]

def detect_xor_cipher(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        best_plaintext = ""
        best_key = None
        best_score = -1

        for line in lines:
            cipher_hex = line.strip()
            ciphertext = bytes.fromhex(cipher_hex)
            result = bruteforce_single_char_xor(ciphertext)
            if result['score'] > best_score:
                best_score = result['score']
                best_plaintext = result['message']
                best_key = result['key']

        return best_plaintext, hex(best_key)

def main():
    file_path = "plain.txt"
    detected_plaintext, key = detect_xor_cipher(file_path)
    print("plaintext: ",detected_plaintext.decode())
    print(f"Key: {key}")


if __name__ == '__main__':
    main()

# Output:
#plaintext: Now that the party is jumping

#Key: 0x35