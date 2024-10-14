def validate_and_strip_pkcs7_padding(plaintext):
    if not plaintext:
        raise ValueError("The plaintext is empty")

    padding_value = plaintext[-1]
    if padding_value < 1 or padding_value > 16:
        raise ValueError("Invalid padding value")

    if plaintext[-padding_value:] != bytes([padding_value]) * padding_value:
        raise ValueError("Invalid PKCS#7 padding")
    return plaintext[:-padding_value]

try:
    result = validate_and_strip_pkcs7_padding(b"ICE ICE BABY\x04\x04\x04\x04")
    print(result.decode())  # output: ICE ICE BABY
except ValueError as e:
    print(e)

try:
    result = validate_and_strip_pkcs7_padding(b"ICE ICE BABY\x05\x05\x05\x05")
    print(result.decode())
except ValueError as e:
    print(e)  # output: Invalid PKCS#7 padding

try:
    result = validate_and_strip_pkcs7_padding(b"ICE ICE BABY\x01\x02\x03\x04")
    print(result.decode())
except ValueError as e:
    print(e)  # output: Invalid PKCS#7 padding