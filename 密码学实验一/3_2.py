def fixed_xor(hex_str1, hex_str2):
    byte_str1 = bytes.fromhex(hex_str1)
    byte_str2 = bytes.fromhex(hex_str2)
    xor_result = bytes([b1 ^ b2 for b1, b2 in zip(byte_str1, byte_str2)])
    hex_result = xor_result.hex()
    return hex_result

hex_str1 = "1c0111001f010100061a024b53535009181c"
hex_str2 = "686974207468652062756c6c277320657965"
xor_result = fixed_xor(hex_str1, hex_str2)
print("XOR Result:", xor_result)

# Output:  XOR Result: 746865206b696420646f6e277420706c6179