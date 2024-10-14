import base64

def hex_to_base64(hex_data):
    base64_string = base64.b64encode(bytes.fromhex(hex_data)).decode('utf-8')
    return base64_string

hex_data = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"  # "Hello World!" in hex
base64_result = hex_to_base64(hex_data)
print("Base64 Encoded:", base64_result)

# Output: Base64 Encoded: SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t