def pkcs7_pad(text, block_size):
    padding_len = block_size - (len(text) % block_size)
    padding = bytes([padding_len] * padding_len)
    return text + padding

def pkcs7_unpad(padded_text, block_size):
    padding_len = padded_text[-1]
    if padding_len > block_size:
        raise ValueError("Invalid padding length")
    return padded_text[:-padding_len]

if __name__ == "__main__":
    block_size = 20
    text = b"YELLOW SUBMARINE"
    
    padded_text = pkcs7_pad(text, block_size)
    print(f"Padded text: {padded_text}")
    
    unpadded_text = pkcs7_unpad(padded_text, block_size)
    print(f"Unpadded text: {unpadded_text}")