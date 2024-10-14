import base64

def English_Scoring(t):
    letter_frequency = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .15000
    }
    return sum([letter_frequency.get(chr(i), 0) for i in t.lower()])  

def Single_XOR(s, single_character):
    t = b''
    for i in s:
        t += bytes([i ^ single_character])
    return t

def ciphertext_XOR(s):
    _data = []
    for single_character in range(256):
        ciphertext = Single_XOR(s, single_character)
        score = English_Scoring(ciphertext)
        data = {
            'Single character': single_character,
            'ciphertext': ciphertext,
            'score': score
        }
        _data.append(data)
    score = sorted(_data, key=lambda score: score['score'], reverse=True)[0]
    return score

def Repeating_key_XOR(_cipher, _key):
    message = b''
    length = len(_key)
    for i in range(len(_cipher)):
        message += bytes([_cipher[i] ^ _key[i % length]])
    return message

def hamming_distance(a, b):
    distance = 0
    for i, j in zip(a, b):
        byte = i ^ j
        distance += sum(k == '1' for k in bin(byte))
    return distance

def Get_the_keysize(ciphertext):
    data = []
    for keysize in range(2, 41):
        block = [ciphertext[i:i + keysize] for i in range(0, len(ciphertext), keysize)]
        distances = []
        for i in range(len(block) - 1):
            block1 = block[i]
            block2 = block[i + 1]
            distance = hamming_distance(block1, block2)
            distances.append(distance / keysize)
        _distance = sum(distances) / len(distances)
        _data = {
            'keysize': keysize,
            'distance': _distance
        }
        data.append(_data)
    _keysize = sorted(data, key=lambda distance: distance['distance'])[0]
    return _keysize

def Break_repeating_key_XOR(ciphertext):
    _keysize = Get_the_keysize(ciphertext)
    keysize = _keysize['keysize']
    print("keysize:", keysize)
    key = b''
    message = b''
    block = [ciphertext[i:i + keysize] for i in range(0, len(ciphertext), keysize)]
    for i in range(keysize):
        new_block = b''
        for j in range(len(block) - 1):
            s = block[j]
            new_block += bytes([s[i]])
        score = ciphertext_XOR(new_block)
        key += bytes([score['Single character']])
    for k in range(len(block)):
        message += Repeating_key_XOR(block[k], key)
    return message, key

if __name__ == '__main__':
    with open('decription.txt', 'r') as of:
        ciphertext = of.read()
        ciphertext = base64.b64decode(ciphertext)
    message, key = Break_repeating_key_XOR(ciphertext)
    print("message:", message.decode('utf-8'), "\nkey:", key.decode('utf-8'))